import tarfile
import rarfile
import zipfile
import os
import json
from datetime import datetime
from pictor.models import Analysis
from pictor.utils.applog_helpers import api_logger
import requests
from pictor.utils.manage_helpers import get_task_interface
from django.utils import timezone


def extract_file(source_file, target_path, extract_type='rar'):
    # 解压分析模块
    try:
        if extract_type == 'rar':
            tar = tarfile.open(source_file)
            tar.extractall(target_path)
            tar.close()
    except Exception as error:
        return error


def task_avg_time(analysis_list):
    # 获取分析任务平均运行时间
    total = analysis_list.count()
    total_minutes = 0
    for analysis in analysis_list:
        minutes = 0
        started_time = analysis.started_time
        finished_time = analysis.finished_time
        if started_time and finished_time:
            minutes = (finished_time - started_time).seconds / 60
        if started_time and not finished_time:
            minutes = (timezone.now() - started_time).seconds / 60
        total_minutes = total_minutes + minutes
    if total:
        avg = round(total_minutes / total, 2)
    else:
        avg = 0
    return avg


def get_headers(token=None):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = token
    return headers


def start_analysis(analysis):
    # 启动分析任务
    url, success_code, error_code = get_task_interface('start_uri')
    serial_number = analysis.serial_number
    if analysis.analysis_module:
        analysis_module_name = analysis.analysis_module.name
        analysis_module_version = analysis.analysis_module.version
        analysis_module_path = analysis.analysis_module.file_uri
    else:
        analysis_module_name = ''
        analysis_module_version = ''
        analysis_module_path = ''
    analysis_parameters = json.loads(analysis.analysis_parameter)
    main_command = analysis.command
    command = f'{main_command} {analysis_module_path}'
    for parameter in analysis_parameters:
        command = f'{command} {parameter["command_tag"]} {parameter["parameter_key"]} {parameter["parameter_value"]}'
    payload = {
        'serial_number': serial_number,
        'command': command,
        'main_command': main_command,
        'analysis_module_name': analysis_module_name,
        'analysis_module_version': analysis_module_version,
        'analysis_module_path': analysis_module_path,
        'analysis_parameters': analysis_parameters,
    }
    api_logger.debug(f'payload: {payload}')
    try:
        resp = requests.post(url, data=json.dumps(payload), headers=get_headers(), timeout=60)
        results = json.loads(resp.text)
        api_logger.debug(f'results: {results}')
        if results.get('code', False):
            if str(results['code']) == success_code:
                api_logger.debug(f'成功启动分析任务, 返回:{results}')
                return True, results['code'], results['messages'], results['results']
            if str(results['code']) == error_code:
                api_logger.warning(f'分析任务启动失败, 返回:{results}')
                return False, results['code'], results['messages'], results['results']
            api_logger.warning(f'启动分析任务获得未知返回码, 返回:{results}')
            return False, 400, '启动分析任务获得未知返回码', results
        else:
            api_logger.warning(f'启动分析任务无法获取返回码, 返回:{results}')
            return False, 400, '启动分析任务无法获取返回码', results
    except Exception as request_error:
        error_messages = f'启动分析任务启请求发生错误:{request_error}'
        api_logger.error(error_messages)
        return False, 500, error_messages, {}


def stop_analysis(analysis):
    # 停止分析任务
    url, success_code, error_code = get_task_interface('stop_uri')
    serial_number = analysis.serial_number
    payload = {
        'serial_number': serial_number,
    }
    try:
        resp = requests.post(url, data=json.dumps(payload), headers=get_headers(), timeout=60)
        results = json.loads(resp.text)
        if results.get('code', False):
            if str(results['code']) == success_code:
                api_logger.debug(f'成功停止分析任务, 返回:{results}')
                return True, results['code'], results['messages'], results['results']
            if str(results['code']) == error_code:
                api_logger.warning(f'分析任务停止失败, 返回:{results}')
                return False, results['code'], results['messages'], results['results']
            api_logger.warning(f'停止分析任务获得未知返回码, 返回:{results}')
            return False, 400, '停止分析任务获得未知返回码', results
        else:
            api_logger.warning(f'停止分析任务无法获取返回码, 返回:{results}')
            return False, 400, '停止分析任务无法获取返回码', results
    except Exception as request_error:
        error_messages = f'停止分析任务请求发生错误:{request_error}'
        api_logger.error(error_messages)
        return False, 500, error_messages, {}


def continue_run_analysis(analysis):
    # 继续分析任务
    url, success_code, error_code = get_task_interface('continue_uri')
    serial_number = analysis.serial_number
    payload = {
        'serial_number': serial_number,
    }
    try:
        resp = requests.post(url, data=json.dumps(payload), headers=get_headers(), timeout=60)
        results = json.loads(resp.text)
        api_logger.debug(f'continue_run results: results')
        if results.get('code', False):
            if str(results['code']) == success_code:
                api_logger.debug(f'成功继续运行分析任务, 返回:{results}')
                return True, results['code'], results['messages'], results['results']
            if str(results['code']) == error_code:
                api_logger.warning(f'分析任务继续运行失败, 返回:{results}')
                return False, results['code'], results['messages'], results['results']
            api_logger.warning(f'继续运行分析任务获得未知返回码, 返回:{results}')
            return False, 400, '停止分析任务获得未知返回码', results
        else:
            api_logger.warning(f'继续运行分析任务无法获取返回码, 返回:{results}')
            return False, 400, '继续运行分析任务无法获取返回码', results
    except Exception as request_error:
        error_messages = f'继续运行分析任务请求发生错误:{request_error}'
        api_logger.error(error_messages)
        return False, 500, error_messages, {}


def reset_analysis(analysis):
    # 重置分析任务
    url, success_code, error_code = get_task_interface('reset_uri')
    serial_number = analysis.serial_number
    payload = {
        'serial_number': serial_number,
    }
    try:
        resp = requests.post(url, data=json.dumps(payload), headers=get_headers(), timeout=60)
        results = json.loads(resp.text)
        if results.get('code', False):
            if str(results['code']) == success_code:
                api_logger.debug(f'成功重置分析任务, 返回:{results}')
                return True, results['code'], results['messages'], results['results']
            if str(results['code']) == error_code:
                api_logger.warning(f'分析任务重置失败, 返回:{results}')
                return False, results['code'], results['messages'], results['results']
            api_logger.warning(f'重置分析任务获得未知返回码, 返回:{results}')
            return False, 400, '重置分析任务获得未知返回码', results
        else:
            api_logger.warning(f'重置分析任务无法获取返回码, 返回:{results}')
            return False, 400, '重置分析任务无法获取返回码', results
    except Exception as request_error:
        error_messages = f'重置分析任务请求发生错误:{request_error}'
        api_logger.error(error_messages)
        return False, 500, error_messages, {}


def get_analysis_status(analysis):
    # 获取分析任务运行转该
    url, success_code, error_code = get_task_interface('status_uri')
    serial_number = analysis.serial_number
    payload = {
        'serial_number': serial_number,
    }
    try:
        resp = requests.post(url, data=json.dumps(payload), headers=get_headers(), timeout=60)
        results = json.loads(resp.text)
        if results.get('code', False):
            if str(results['code']) == success_code:
                api_logger.debug(f'成功获取分析任务状态, 返回:{results}')
                return True, results['code'], results['messages'], results['results']
            if str(results['code']) == error_code:
                api_logger.warning(f'分析任务获取状态失败, 返回:{results}')
                return False, results['code'], results['messages'], results['results']
            api_logger.warning(f'获取分析任务状态获得未知返回码, 返回:{results}')
            return False, 400, '获取分析任务状态获得未知返回码', results
        else:
            api_logger.warning(f'获取分析任务状态无法获取返回码, 返回:{results}')
            return False, 400, '获取分析任务状态无法获取返回码', results
    except Exception as request_error:
        error_messages = f'获取分析任务状态请求发生错误:{request_error}'
        api_logger.error(error_messages)
        return False, 500, error_messages, {}


def get_analysis_results(analysis):
    # 获取分析任务结果
    url, success_code, error_code = get_task_interface('result_uri')
    serial_number = analysis.serial_number
    payload = {
        'serial_number': serial_number,
    }
    try:
        resp = requests.post(url, data=json.dumps(payload), headers=get_headers(), timeout=60)
        results = json.loads(resp.text)
        if results.get('code', False):
            if str(results['code']) == success_code:
                api_logger.debug(f'成功获取分析任务结果, 返回:{results}')
                return True, results['code'], results['messages'], results['results']
            if str(results['code']) == error_code:
                api_logger.warning(f'分析任务获取结果失败, 返回:{results}')
                return False, results['code'], results['messages'], results['results']
            api_logger.warning(f'获取分析任务结果获得未知返回码, 返回:{results}')
            return False, 400, '获取分析任务结果获得未知返回码', results
        else:
            api_logger.warning(f'获取分析任务结果无法获取返回码, 返回:{results}')
            return False, 400, '获取分析任务结果无法获取返回码', results
    except Exception as request_error:
        error_messages = f'获取分析任务结果请求发生错误:{request_error}'
        api_logger.error(error_messages)
        return False, 500, error_messages, {}


def get_analysis_logs(analysis):
    # 获取分析任务运行日志
    url, success_code, error_code = get_task_interface('log_uri')
    serial_number = analysis.serial_number
    payload = {
        'serial_number': serial_number,
    }
    try:
        resp = requests.post(url, data=json.dumps(payload), headers=get_headers(), timeout=60)
        api_logger.debug(f'resp, 返回:{resp}')
        results = json.loads(resp.text)
        api_logger.debug(f'results, 返回:{results}')
        if results.get('code', False):
            if str(results['code']) == success_code:
                api_logger.debug(f'成功获取分析任务运行日志, 返回:{results}')
                return True, results['code'], results['messages'], results['results']
            if str(results['code']) == error_code:
                api_logger.warning(f'分析任务获取运行日志失败, 返回:{results}')
                return False, results['code'], results['messages'], results['results']
            api_logger.warning(f'获取分析任务运行日志获得未知返回码, 返回:{results}')
            return False, 400, '获取分析任务运行日志获得未知返回码', results
        else:
            api_logger.warning(f'获取分析任务日志无法获取返回码, 返回:{results}')
            return False, 400, '获取分析任务日志无法获取返回码', results
    except Exception as request_error:
        error_messages = f'获取分析任务运行日志请求发生错误:{request_error}'
        api_logger.error(error_messages)
        return False, 500, error_messages, {}

