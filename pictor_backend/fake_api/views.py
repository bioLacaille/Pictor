from rest_framework import viewsets, mixins, filters, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from fake_api.tests import fake_log


class AnalysisTaskViewSet(viewsets.ViewSet):
    permission_classes = ()
    """
    ## 參數：
       serial_number: string, 必需, 分析任務编号
       command： 完整运行命令, string, 必需, 由 main_command 与 analysis_parameter 组成的运行命令
       main_command: dict, 可空, 模块对应运行的主命令,
       analysis_module_name: dict, 可空, 所属分析模块名称
       analysis_module_version: dict, 可空, 所属分析模块版本
       analysis_module_path: string, 可空, 所属分析模块所在的路径
       analysis_parameter: dict, 可空, 分析参数,
    ## 响应:
        code: 必需, 返回码
        messages: 可空, 返回信息
        results: 可空, 返回结果
    """
    @action(methods=['post'], detail=False)
    def start(self, request, *args, **kwargs):
        serial_number = request.data.get('serial_number', '')
        command = request.data.get('command', '')
        analysis_module_name = request.data.get('analysis_module_name', '')
        analysis_module_version = request.data.get('analysis_module_version', '')
        analysis_module_path = request.data.get('analysis_module_path', '')
        analysis_parameter = request.data.get('analysis_parameter', '')
        result = {'code': 200, 'messages': f'test!启动分析任务', 'results': {}}
        return Response(result, status=status.HTTP_200_OK)

    """
    ## 參數：
       serial_number: string, 必需, 分析任務编号
    ## 响应:
        code: 必需, 返回码
        messages: 可空, 返回信息
        results: 可空, 返回结果
    """
    @action(methods=['post'], detail=False)
    def stop(self, request, *args, **kwargs):
        serial_number = request.data.get('serial_number', '')
        result = {'code': 200, 'messages': f'test!停止分析任务', 'results': {}}
        return Response(result, status=status.HTTP_200_OK)

    """
    ## 參數：
       serial_number: string, 必需, 分析任務编号
    ## 响应:
        code: 必需, 返回码
        messages: 可空, 返回信息
        results: 可空, 返回结果
    """
    @action(methods=['post'], detail=False)
    def continue_run(self, request, *args, **kwargs):
        serial_number = request.data.get('serial_number', '')
        result = {'code': 200, 'messages': f'test!继续分析任务', 'results': {}}
        return Response(result, status=status.HTTP_200_OK)

    """
    ## 參數：
       serial_number: string, 必需, 分析任務编号
    ## 响应:
        code: 必需, 返回码
        messages: 可空, 返回信息
        results: 可空, 返回结果
    """
    @action(methods=['post'], detail=False)
    def reset(self, request, *args, **kwargs):
        serial_number = request.data.get('serial_number', '')
        result = {'code': 200, 'messages': f'test!重置分析任务', 'results': {}}
        return Response(result, status=status.HTTP_200_OK)

    """
    ## 參數：
       serial_number: string, 必需, 分析任務编号
    ## 响应:
        code: 必需, 返回码
        messages: 可空, 返回信息
        results: 必需, 返回分析任务状态
        # 分析状态
        ANALYSIS_PENDING = 0
        ANALYSIS_UN_START = 10
        ANALYSIS_RUNNING = 20
        ANALYSIS_STOP = 30
        ANALYSIS_ERROR = 40
        ANALYSIS_SUCCESS = 50
        ANALYSIS_RESET = 60
        ANALYSIS_STATUS = {
            ANALYSIS_PENDING: '等待中',
            ANALYSIS_UN_START: '未启动',
            ANALYSIS_RUNNING: '进行中',
            ANALYSIS_STOP: '已停止',
            ANALYSIS_ERROR: '错误结束',
            ANALYSIS_SUCCESS: '成功结束',
            ANALYSIS_RESET: '已重置',
        }
    """
    @action(methods=['post'], detail=False)
    def status(self, request, *args, **kwargs):
        serial_number = request.data.get('serial_number', '')
        result = {'code': 200, 'messages': f'test!分析任务状态', 'results': {}}
        return Response(result, status=status.HTTP_200_OK)

    """
    ## 參數：
       serial_number: string, 必需, 分析任務编号
    ## 响应:
        code: 必需, 返回码
        messages: 可空, 返回信息
        results: 必需, 返回结果, 暂未确定数据格式
    """
    @action(methods=['post'], detail=False)
    def results(self, request, *args, **kwargs):
        serial_number = request.data.get('serial_number', '')
        result = {'code': 200, 'messages': f'test!分析任务结果', 'results': {}}
        return Response(result, status=status.HTTP_200_OK)

    """
    ## 參數：
       serial_number: string, 必需, 分析任務编号
    ## 响应:
        code: 必需, 返回码
        messages: 可空, 返回信息
        results: 必需, 日志内容
    """
    @action(methods=['post'], detail=False)
    def logs(self, request, *args, **kwargs):
        serial_number = request.data.get('serial_number', '')
        result = {'code': 200, 'messages': f'test!分析任务日志', 'results': fake_log}
        return Response(result, status=status.HTTP_200_OK)


