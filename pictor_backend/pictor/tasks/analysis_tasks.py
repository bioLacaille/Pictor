from celery import shared_task
from pictor.models import User, DataSet, AnalysisModule
from pictor.utils.applog_helpers import task_logger
import shutil
import os
import git
from pictor.configures import GIT, LOCAL, MODULE_ACTIVE, MODULE_ERROR


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
                pass
    except Exception as error:
        module.status = MODULE_ERROR
        module.save()
        task_logger.error(f'安装分析模块发生错误:{error}')


# todo 定时任务(分析模块/分析任务)