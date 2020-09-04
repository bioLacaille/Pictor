"""
系統日志记录
"""
import os
from loguru import logger
from pictor.utils.base_heplers import create_or_get_directory
from pictor.utils.setup_helpers import get_configure


def make_filter(name):

    def filter_record(record):
        return record["extra"].get("name") == name

    return filter_record


base_log_path = get_configure('SYSTEM_SETTING', 'LOG_PATH', '/tmp/pictor')
base_log_path = create_or_get_directory(base_log_path)

api_log_path = os.path.join(base_log_path, 'pictor_api.log')
task_log_path = os.path.join(base_log_path, 'pictor_task.log')

logger.add(api_log_path, level="DEBUG", filter=make_filter("api"))
logger.add(task_log_path, level="DEBUG", filter=make_filter("task"))

api_logger = logger.bind(name="api")
task_logger = logger.bind(name="task")
