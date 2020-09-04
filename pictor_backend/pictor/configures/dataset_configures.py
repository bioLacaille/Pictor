"""
Author: Alan Fu
Email: fualan1990@gmail.com
数据模块所需配置
"""
PUBLIC_DATA = 10
SAMPLE_DATA = 20
PROJECT_DATA = 30
DATABASE_DATA = 40
SEQ_DATA = 50
INTERMEDIATE_DATA = 60

FILE = 10
DIRECTORY = 20

DATASET_TYPE = {
    PUBLIC_DATA: 'public',
    SAMPLE_DATA: 'sample',
    PROJECT_DATA: 'project',
    DATABASE_DATA: 'database',
    SEQ_DATA: 'sequencing',
    INTERMEDIATE_DATA: 'intermediate'
}

DATASET_TYPE_ZH = {
    PUBLIC_DATA: '公共数据',
    SAMPLE_DATA: '样本数据',
    PROJECT_DATA: '项目数据',
    DATABASE_DATA: '数据集',
    SEQ_DATA: '测序数据',
    INTERMEDIATE_DATA: '中间文件'
}

DATASET_PATH = {
    PUBLIC_DATA: 'Public',  # PictorBio/Public/
    SAMPLE_DATA: 'Samples',  # PictorBio/Samples/{工作区}/
    PROJECT_DATA: 'Projects',  # PictorBio/Projects/{工作区}/
    DATABASE_DATA: 'DataSet',  # PictorBio/DataSet/{工作区}/
    SEQ_DATA: 'SeqData',  # PictorBio/SeqData
    INTERMEDIATE_DATA: 'Analyses'  # PictorBio/Analyses/{工作区}/
}

FILE_TYPE = {
    FILE: 'file',
    DIRECTORY: 'directory',
}

FILE_TYPE_ZH = {
    FILE: '文件',
    DIRECTORY: '目录',
}



