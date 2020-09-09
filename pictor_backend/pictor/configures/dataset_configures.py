"""
Author: Alan Fu
Email: fualan1990@gmail.com
文件数据模块所需配置
"""
PUBLIC_DATA = 10
SAMPLE_DATA = 20
PROJECT_DATA = 30
DATABASE_DATA = 40

FILE = 10
DIRECTORY = 20

UPLOAD = 10  # 上传
DOWNLOAD = 20  # 下载
GENERATE = 30  # 生成

DATASET_TYPE = {
    PUBLIC_DATA: 'public',
    SAMPLE_DATA: 'sample',
    PROJECT_DATA: 'project',
    DATABASE_DATA: 'database',
}

DATASET_TYPE_ZH = {
    PUBLIC_DATA: '公共数据',
    SAMPLE_DATA: '样本数据',
    PROJECT_DATA: '项目数据',
    DATABASE_DATA: '数据库',
}

DATASET_PATH = {
    PUBLIC_DATA: 'Public',
    SAMPLE_DATA: 'Samples',
    PROJECT_DATA: 'Projects',
    DATABASE_DATA: 'Database',
}

FILE_TYPE = {
    FILE: 'file',
    DIRECTORY: 'directory',
}

FILE_TYPE_ZH = {
    FILE: '文件',
    DIRECTORY: '目录',
}

SOURCE_TYPE = {
    UPLOAD: 'upload',
    DOWNLOAD: 'download',
    GENERATE: 'generate',
}

SOURCE_TYPE_zh = {
    UPLOAD: '上传',
    DOWNLOAD: '离线下载',
    GENERATE: '本地生成',
}