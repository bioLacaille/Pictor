from celery import shared_task
from pictor.models import User, DataSet, AnalysisModule, Analysis
from pictor.utils.applog_helpers import task_logger
from pictor.utils.analysis_helpers import get_analysis_status
import shutil
import json
import os
import git
import datetime
from pictor.configures import GIT, LOCAL, MODULE_ACTIVE, MODULE_ERROR, ANALYSIS_PENDING, ANALYSIS_UN_START, \
    ANALYSIS_RUNNING, ANALYSIS_STOP, ANALYSIS_ERROR, ANALYSIS_SUCCESS, ANALYSIS_RESET, PROJECT_DATA
from pictor.utils.tar_helpers import un_rar_file, un_zip_file, un_tar_file
from pictor.utils.dataset_helpers import create_file_records, get_data_directory_path, create_dir_record


@shared_task(name="analysis_module_install_task")
def analysis_module_install_task(module_id):
    module = AnalysisModule.objects.get(pk=int(module_id))
    try:
        if module.module_type == GIT:
            version_split = module.version.split('/')
            version = version_split[2]
            clone_path = module.file_path
            task_logger.debug(f'安装github模块: {module.name}, {module.version}, {clone_path}')
            repo = git.Repo.clone_from(module.url, clone_path)
            repo.git.checkout(version)
            module.status = MODULE_ACTIVE
            module.save()
        if module.module_type == LOCAL:
            file_path = module.file_path
            file_name, file_extension = os.path.splitext(os.path.basename(module.pipeline_file.path))
            if 'tar' in file_extension:
                task_logger.debug(f'安装本地 tar 模块: {module.name}, {module.version}, {file_path}')
                un_tar_file(module.pipeline_file.path, file_path)
                module.status = MODULE_ACTIVE
                module.save()
            elif 'zip' in file_extension:
                task_logger.debug(f'安装本地 zip 模块: {module.name}, {module.version}, {file_path}')
                un_zip_file(module.pipeline_file.path, file_path)
                module.status = MODULE_ACTIVE
                module.save()
            elif 'rar' in file_extension:
                task_logger.debug(f'安装本地 rar 模块: {module.name}, {module.version}, {file_path}')
                un_rar_file(module.pipeline_file.path, file_path)
                module.status = MODULE_ACTIVE
                module.save()
    except Exception as error:
        module.status = MODULE_ERROR
        module.save()
        task_logger.error(f'安装分析模块发生错误:{error}')


@shared_task(name='check_analysis_running_status')
def check_analysis_running_status():
    """检查分析任务运行状态"""
    analysis_list = Analysis.objects.filter(status=ANALYSIS_RUNNING).all()
    task_logger.info("检查分析任务")
    for analysis in analysis_list:
        is_success, code, messages, results = get_analysis_status(analysis)
        if is_success:
            status = results['status']
            process = results['process']
            if status == ANALYSIS_RUNNING:  # 正在运行
                task_logger.info(f'分析任务:{analysis.serial_number}正在运行中, 尚未结束')
            elif status == ANALYSIS_ERROR:
                analysis.status = ANALYSIS_ERROR  # 错误结束
                analysis.process = process
                analysis.finished_time = datetime.datetime.now()
                analysis.save()
                task_logger.info(f'分析任务:{analysis.serial_number}错误结束,  错误信息:{messages}, 返回结果:{results}')
                # 生成文件记录
                if analysis.project:
                    project_number = analysis.project.serial_number
                else:
                    project_number = 'NoProject'
                create_dir_record(instance=analysis, data_type=PROJECT_DATA, work_zone=analysis.work_zone,
                                  current_path=f'{project_number}')
                create_dir_record(instance=analysis, data_type=PROJECT_DATA, work_zone=analysis.work_zone,
                                  current_path=f'{project_number}/{analysis.serial_number}')
                create_file_records(instance=analysis, data_type=PROJECT_DATA, work_zone=analysis.work_zone,
                                    current_path=f'{project_number}/{analysis.serial_number}')
                # todo 发送站内新或邮件通知
            elif status == ANALYSIS_SUCCESS:
                # 测试数据, todo: 正式上线后移除
                try:
                    import subprocess, time
                    if analysis.project:
                        project_number = analysis.project.serial_number
                    else:
                        project_number = 'NoProject'
                    file_path = '/home/alan/test/results/*'
                    target_directory = get_data_directory_path(PROJECT_DATA,
                                                               f'{project_number}/{analysis.serial_number}',
                                                               analysis.work_zone.id)
                    if not os.path.exists(target_directory):
                        task_logger.debug(f'复制测试数据, 创建目录 {target_directory}')
                        os.makedirs(target_directory, exist_ok=True)
                    time.sleep(3)
                    task_logger.debug(f'复制测试数据, rsync -aP {file_path} {target_directory}')
                    subprocess.check_output(f'rsync -aP {file_path} {target_directory}', shell=True)
                except Exception as error:
                    task_logger.error(f'复制测试数据失败:{error}')
                analysis.status = ANALYSIS_SUCCESS  # 正常结束
                analysis.process = process
                analysis.finished_time = datetime.datetime.now()
                analysis.save()
                task_logger.info(f'分析任务:{analysis.serial_number}成功结束')
                # 生成文件记录
                if analysis.project:
                    project_number = analysis.project.serial_number
                else:
                    project_number = 'NoProject'
                create_dir_record(instance=analysis, data_type=PROJECT_DATA, work_zone=analysis.work_zone,
                                  current_path=f'{project_number}')
                create_dir_record(instance=analysis, data_type=PROJECT_DATA, work_zone=analysis.work_zone,
                                  current_path=f'{project_number}/{analysis.serial_number}')
                create_file_records(instance=analysis, data_type=PROJECT_DATA, work_zone=analysis.work_zone,
                                    current_path=f'{project_number}/{analysis.serial_number}')
                # todo 发送站内新或邮件通知
            elif status == ANALYSIS_STOP:
                analysis.status = ANALYSIS_STOP
                analysis.finished_time = datetime.datetime.now()
                analysis.save()
                task_logger.info(f'分析任务:{analysis.serial_number}已停止或被停止')
                # 生成文件记录
                if analysis.project:
                    project_number = analysis.project.serial_number
                else:
                    project_number = 'NoProject'
                create_dir_record(instance=analysis, data_type=PROJECT_DATA, work_zone=analysis.work_zone,
                                  current_path=f'{project_number}')
                create_dir_record(instance=analysis, data_type=PROJECT_DATA, work_zone=analysis.work_zone,
                                  current_path=f'{project_number}/{analysis.serial_number}')
                create_file_records(instance=analysis, data_type=PROJECT_DATA, work_zone=analysis.work_zone,
                                    current_path=f'{project_number}/{analysis.serial_number}')
                # todo 发送站内新或邮件通知
        else:
            task_logger.error(f'分析任务:{analysis.serial_number} 查询状态失败: {is_success}, {code}, {messages}, {results}')
