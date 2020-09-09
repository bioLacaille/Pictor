"""
Author: Alan Fu
Email: fualan1990@gmail.com
操作日志模块所需配置
"""
AUTH_ACTION_TYPE = 10
CREATE_ACTION_TYPE = 100
UPDATE_ACTION_TYPE = 110
DELETE_ACTION_TYPE = 120
BULK_CREATE_ACTION_TYPE = 200
BULK_UPDATE_ACTION_TYPE = 210
BULK_DELETE_ACTION_TYPE = 230
UPLOAD_ACTION_TYPE = 300
START_ACTION_TYPE = 400
STOP_ACTION_TYPE = 410
CONTINUE_ACTION_TYPE = 420
RESET_ACTION_TYPE = 430
ACTIVE_ACTION_TYPE = 500
DISABLE_ACTION_TYPE = 510
READ_NOTIFY_ACTION_TYPE = 600
UNREAD_NOTIFY_ACTION_TYPE = 610
DELETE_NOTIFY_ACTION_TYPE = 620
RECOVER_NOTIFY_ACTION_TYPE = 630
CLEAR_NOTIFY_ACTION_TYPE = 640

ACTION_TYPE = {
    AUTH_ACTION_TYPE: '认证',
    CREATE_ACTION_TYPE: '新增',
    UPDATE_ACTION_TYPE: '修改',
    DELETE_ACTION_TYPE: '删除',
    BULK_CREATE_ACTION_TYPE: '批量新增',
    BULK_UPDATE_ACTION_TYPE: '批量修改',
    BULK_DELETE_ACTION_TYPE: '批量删除',
    START_ACTION_TYPE: '启动任务',
    STOP_ACTION_TYPE: '停止任务',
    RESET_ACTION_TYPE: '重置任务',
    UPLOAD_ACTION_TYPE: '上传文件',
    ACTIVE_ACTION_TYPE: '启用',
    DISABLE_ACTION_TYPE: '禁用',
    READ_NOTIFY_ACTION_TYPE: '标记已读消息',
    UNREAD_NOTIFY_ACTION_TYPE: '标记未读消息',
    DELETE_NOTIFY_ACTION_TYPE: '标记删除消息',
    RECOVER_NOTIFY_ACTION_TYPE: '恢复消息',
    CLEAR_NOTIFY_ACTION_TYPE: '清空消息',
}