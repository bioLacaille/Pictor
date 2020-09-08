import os
import hashlib
from pathlib import Path
import uuid
import glob
from django.conf import settings
from pictor.models.workzone_models import WorkZone
from pictor.utils.base_heplers import create_or_get_directory
from pictor.configures.dataset_configures import *
import subprocess


def get_data_directory_path(data_type, current_path, work_zone_id):
    # 获取完整目录路径
    data_type = int(data_type)
    work_zone_id = int(work_zone_id)
    # 根目录
    data_path = create_or_get_directory(os.path.join(settings.MEDIA_ROOT, DATASET_PATH[data_type]))
    # 若不是公共数据, 则数据保存在工作区下
    if data_type != 10 and work_zone_id:
        work_zone = WorkZone.objects.get(pk=work_zone_id)
        data_path = os.path.join(data_path, work_zone.serial_number)
    # 当前相对路径
    if current_path:
        data_path = os.path.join(data_path, current_path)
    create_or_get_directory(data_path)
    return data_path


def get_data_path(data_type, current_path, work_zone_id, file_name):
    # 获取完整文件路径
    data_directory_path = get_data_directory_path(data_type, current_path, work_zone_id)
    data_path = os.path.join(data_directory_path, file_name)
    return data_path


def get_data_uri(data_type, current_path, work_zone_id, file_name):
    # 获取可用访问的相对路径
    data_type = int(data_type)
    base_path = os.path.join(settings.MEDIA_URL, DATASET_PATH[data_type])
    # 若不是公共数据, 则数据保存在工作区下
    if data_type != 10:
        work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        base_path = os.path.join(base_path, work_zone.serial_number)
    # 当前路径
    if current_path:
        base_path = os.path.join(base_path, current_path)
    data_uri = os.path.join(base_path, file_name)
    return data_uri


def get_file_path_md5(file_path):
    # 获取文件MD5
    try:
        m = hashlib.md5()
        m.update(f"{file_path}".encode("utf-8"))
        return m.hexdigest()
    except:
        return str(uuid.uuid1())


def get_data_files(dataset):
    # 根目录
    data_files = []
    for data in dataset:
        data_files.append({"Id": data.id, "ProjectId": data.serial_number, "IdentityId": data.serial_number,
                           "RourceId": data.serial_number, "WBSId": data.serial_number, "FileId": data.serial_number,
                           "ParentId": get_file_path_md5(data.directory_path), "Parents": data.directory_path,
                           "Name": data.file_name, "Size": data.file_size,
                           "SuffixName": Path(data.file_name).suffix.replace(".", ""),
                           "FullPath": data.relative_path,
                           "FullUri": data.file_uri,
                           "Type": data.file_type, "FileType": data.file_type, "RourceType": data.file_type,
                           "ISAllVisible": data.uploaded, "Describe": "",
                           "CreateUserName": data.creator.nickname, "CreateTime": data.created_time, "EditTime": data.edit_time,
                           "EditBy": data.creator.nickname,
                           "PictuerCount": 0, "FilesCount": 0,
                           "PermissionType": 0})
    return data_files


def check_md5_sum(file_name, hash_factory=hashlib.md5, chunk_num_blocks=128):
    h = hash_factory()
    with open(file_name, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_num_blocks*h.block_size), b''):
            h.update(chunk)
    return h.hexdigest()


def get_file_size(path):
    """取得文件夹大小:KB"""
    try:
        if os.path.isfile(path):
            return os.path.getsize(path) / 1024
        else:
            size = float(subprocess.check_output(['du', '-s', path]).split()[0].decode('utf-8'))
    except:
        size = 0
    return size


def create_dir_record(instance, data_type=PUBLIC_DATA, work_zone=None, current_path=''):
    from pictor.models.dataset_models import DataSet
    base_path = get_data_directory_path(data_type, current_path, work_zone.id)
    file_name = os.path.basename(base_path)
    file_size = get_file_size(base_path)
    if not DataSet.objects.filter(directory_path=os.path.dirname(current_path), file_name=file_name,
                                  data_type=data_type, file_type=DIRECTORY, work_zone=work_zone).first():
        DataSet.objects.create(directory_path=os.path.dirname(current_path), file_name=file_name, data_type=data_type,
                               file_type=DIRECTORY, file_size=file_size, uploaded=True, file_md5='',
                               uploaded_chunks=1, total_chunks=1, source_type=GENERATE,
                               work_zone=work_zone, creator=instance.creator)


def create_file_records(instance, data_type=PUBLIC_DATA, work_zone=None, current_path=''):
    from pictor.models.dataset_models import DataSet
    base_path = get_data_directory_path(data_type, current_path, work_zone.id)
    all_files = glob.glob(f'{base_path}/*')
    for all_file in all_files:
        file_name = os.path.basename(all_file)
        file_size = get_file_size(all_file)
        if os.path.isdir(all_file):
            DataSet.objects.create(directory_path=current_path,
                                   file_name=file_name, data_type=data_type,
                                   file_type=DIRECTORY, file_size=file_size, uploaded=True, file_md5='',
                                   uploaded_chunks=1, total_chunks=1, source_type=GENERATE,
                                   work_zone=work_zone, creator=instance.creator)
            create_file_records(instance, data_type=data_type, work_zone=work_zone,
                                current_path=os.path.join(current_path, file_name))
        else:
            file_md5 = check_md5_sum(all_file)
            DataSet.objects.create(directory_path=current_path,
                                   file_name=file_name, data_type=data_type,
                                   file_type=FILE, file_size=file_size, uploaded=True, file_md5=file_md5,
                                   uploaded_chunks=1, total_chunks=1, source_type=GENERATE,
                                   work_zone=work_zone, creator=instance.creator)
