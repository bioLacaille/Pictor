from celery.schedules import crontab
from pictor.utils.setup_helpers import get_configure

redis_host = get_configure('REDIS', 'REDIS_HOST', '127.0.0.1')
redis_port = get_configure('REDIS', 'REDIS_PORT', '6379')
redis_db_num = get_configure('REDIS', 'REDIS_DB_NUM', '1')
redis_password = get_configure('REDIS', 'REDIS_PASSWORD', None)

redis_url = f'redis://{redis_host}:{redis_port}/{redis_db_num}'

#  CELERY定时任务

CELERY_BROKER_URL = redis_url
CELERY_RESULT_BACKEND = redis_url
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'

# todo 将定时任务转为页面配置
CELERY_BEAT_SCHEDULE = {
    # 检查任务
    'check_analysis_running_status': {
        'task': 'check_analysis_running_status',
        'schedule': 30
    },
}
