from pictor.configures import DELETE_ACTION_TYPE, BULK_DELETE_ACTION_TYPE
from pictor.models import AnalysisTaskInterface
from datetime import datetime
from pictor.utils.applog_helpers import api_logger
import json
import urllib.parse

DELETE_URI = {
    'domain': 'http://127.0.0.1:8888/fake_api/analysis_tasks/',
    'success_code': '200',
    'error_code': '400',
    'start_uri': 'start',
    'stop_uri': 'stop_',
    'continue_uri': 'continue_run',
    'reset_uri': 'reset',
    'status_uri': 'status',
    'result_uri': 'results',
    'log_uri': 'logs',
}


def get_task_interface(uri_type='start_uri'):
    task_interface = AnalysisTaskInterface.objects.get_active().first()
    api_logger.debug(f'get_task_interface : {task_interface}')
    if task_interface:
        domain = task_interface.domain
        if not domain.endswith('/'):
            domain = f'{domain}/'
        api_logger.debug(f'get_task_interface domain: {task_interface.domain}')
        uri = getattr(task_interface, uri_type, '')
        api_logger.debug(f'get_task_interface uri: {uri}')
        url = urllib.parse.urljoin(domain, uri)
        api_logger.debug(f'get_task_interface url: {url}')
        success_code = task_interface.success_code
        error_code = task_interface.error_code
    else:
        domain = DELETE_URI['domain']
        uri = DELETE_URI[uri_type]
        url = urllib.parse.urljoin(domain, uri)
        success_code = DELETE_URI['success_code']
        error_code = DELETE_URI['error_code']
    if not url.endswith('/'):
        url = f'{url}/'
    api_logger.debug(f'{url}')
    return url, success_code, error_code