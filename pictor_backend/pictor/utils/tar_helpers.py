import tarfile
import rarfile
import zipfile
import os


def un_tar_file(file_path, target_path, tar_type='r'):
    with tarfile.open(file_path, tar_type) as tar:
        tar.extractall(path=target_path)


def un_zip_file(file_path, target_path):
    with zipfile.ZipFile(file_path, 'r') as z:
        z.extractall(target_path)


def un_rar_file(file_path, target_path):
    with rarfile.RarFile(file_path, 'r') as z:
        z.extractall(target_path)


def tar_file(file_path, target_path, tar_type='w'):
    tar_directory = os.path.dirname(target_path)
    if not os.path.exists(tar_directory):
        os.makedirs(tar_directory, exist_ok=True)
    tar = tarfile.open(target_path, tar_type)
    for root, directory, files in os.walk(file_path):
        # 取得相对路径
        root_ = os.path.relpath(root, start=os.path.dirname(file_path))
        for file in files:
            full_path = os.path.join(root, file)
            try:
                tar.add(full_path, arcname=os.path.join(root_, file))
            except Exception as error:
                print(f'添加压缩文件发生错误:{error}')
    tar.close()


def zip_file(file_path, target_path):
    tar_directory = os.path.dirname(target_path)
    if not os.path.exists(tar_directory):
        os.makedirs(tar_directory, exist_ok=True)
    f = zipfile.ZipFile(target_path, 'w', zipfile.ZIP_DEFLATED)
    for root, directory, files in os.walk(file_path):
        root_ = os.path.relpath(root, start=os.path.dirname(file_path))
        for file in files:
            full_path = os.path.join(root, file)
            try:
                f.write(full_path, arcname=os.path.join(root_, file))
            except Exception as error:
                print(f'添加压缩文件发生错误:{error}')

    f.close()


def rar_file(file_path, target_path):
    pass


if __name__ == '__main__':
    source_file = '/home/alan/test/test'
    tar_gz_f = '/home/alan/test/test.tar.gz'
    tar_bz2_f = '/home/alan/test/test.tar.bz2'
    tar_xz_f = '/home/alan/test/test.tar.xz'
    tar_f = '/home/alan/test/test.tar'
    zip_f = '/home/alan/test/test.zip'
    rar_f = '/home/alan/test/test.rar'
    # tar_file(source_file, tar_gz_f, tar_type='w:gz')
    # tar_file(source_file, tar_bz2_f, tar_type='w:bz2')
    # tar_file(source_file, tar_xz_f, tar_type='w:xz')
    # tar_file(source_file, tar_f, tar_type='w')
    # zip_file(source_file, zip_f)
    # un_tar_file(tar_f, os.path.dirname(source_file))
    un_zip_file(zip_f, os.path.dirname(source_file))
    # un_rar_file(rar_f, os.path.dirname(source_file))

