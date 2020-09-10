"""
Author: Alan Fu
Email: fualan1990@gmail.com
操作权限配置
"""

WORK_ZONE_PERMISSION = {
    'edit': False,  # 修改
    'change_member': False,  # 调整成员
    'delete': False,  # 删除
}

PROJECT_PERMISSION = {
    'add': False,  # 新增
    'edit': False,  # 修改
    'delete': False,  # 删除
    'manage': False,  # 管理
}

SAMPLE_PERMISSION = {
    'add': False,  # 新增
    'edit': False,  # 修改
    'delete': False,  # 删除
    'related': False,  # 关联
}

DATASET_PERMISSION = {
    'upload': False,  # 上传
    'create_directory': False,  # 创建文件夹
    'delete': False,  # 删除文件/文件夹
    'download': False,  # 离线上传
    'rename': False,  # 重命名
    'copy': False,  # 复制
    'move': False,  # 移动
}

ANALYSIS_PERMISSION = {
    'add': False,  # 新增
    'edit': False,  # 修改
    'delete': False,  # 删除
    'start': False,  # 启动
    'stop': False,  # 停止
    'continue': False,  # 继续
    'reset': False,  # 重置
}

NUMBER_SETTING_PERMISSION = {
    'add': False,  # 新增
    'edit': False,  # 修改
    'delete': False,  # 删除
    'active': False,  # 启用/禁用
}

ACTION_PERMISSION = {
    'work_zone': WORK_ZONE_PERMISSION,
    'project': PROJECT_PERMISSION,
    'sample': SAMPLE_PERMISSION,
    'dataset': DATASET_PERMISSION,
}