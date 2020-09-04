from celery import shared_task
from pictor.models import User, DataSet
from pictor.utils.applog_helpers import task_logger
import shutil
import os
from pictor.utils.dataset_helpers import get_data_directory_path
from distutils.dir_util import copy_tree
from pictor.configures import DIRECTORY, FILE


@shared_task(name="copy_dataset_task")
def copy_move_dataset_task(dataset_ids, data_type, target_path, move=False):
    # 复制/移动文件或文件夹
    try:
        for dataset_id in dataset_ids:
            dataset = DataSet.objects.get(pk=int(dataset_id))
            file_full_path = dataset.file_full_path
            target_directory_path = get_data_directory_path(data_type=data_type, current_path=target_path,
                                                            work_zone_id=None)
            target_full_path = os.path.join(target_directory_path, os.path.basename(file_full_path))
            if dataset.file_type == FILE:
                if move:
                    task_logger.debug(f'移动文件:{file_full_path} 到 {target_full_path}')
                    shutil.move(file_full_path, target_full_path)
                else:
                    task_logger.debug(f'复制文件:{file_full_path} 到 {target_full_path}')
                    shutil.copyfile(file_full_path, target_full_path)
            if dataset.file_type == DIRECTORY:
                if move:
                    task_logger.debug(f'移动文件夹:{file_full_path} 到 {target_full_path}')
                    shutil.move(file_full_path, target_full_path)
                else:
                    task_logger.debug(f'复制文件夹:{file_full_path} 到 {target_full_path}')
                    copy_tree(file_full_path, target_full_path)
    except Exception as error:
        task_logger.error(f'复制/移动文件或文件夹发生错误:{error}')
