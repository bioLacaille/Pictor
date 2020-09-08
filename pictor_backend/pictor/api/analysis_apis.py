from rest_framework import viewsets, mixins, filters, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from pictor.models import AnalysisModule, Analysis, AnalysisParameter, WorkZone, Project
from pictor.serializers.analysis_serializers import AnalysisModuleActionSerializer, AnalysisModuleListSerializer, \
    AnalysisModuleDetailSerializer, AnalysisActionSerializer, AnalysisListSerializer, AnalysisDetailSerializer, \
    AnalysisParameterDetailSerializer, AnalysisParameterActionSerializer, AnalysisParameterListSerializer
import git
import os
import shutil
from datetime import datetime
from pictor.utils.applog_helpers import api_logger
from pictor.utils.actionlog_helpers import action_log
from pictor.configures import CREATE_ACTION_TYPE, UPDATE_ACTION_TYPE, DELETE_ACTION_TYPE,  BULK_DELETE_ACTION_TYPE, \
    ANALYSIS_MODULE_TYPE, ANALYSIS_MODULE_STATUS, ANALYSIS_STATUS, GIT, LOCAL, MODULE_DOING, MODULE_UN_ACTIVE, \
    MODULE_UN_DONE, ANALYSIS_PENDING, ANALYSIS_UN_START, ANALYSIS_RUNNING, ANALYSIS_STOP, ANALYSIS_ERROR, \
    ANALYSIS_SUCCESS, ANALYSIS_RESET, START_ACTION_TYPE, STOP_ACTION_TYPE, RESET_ACTION_TYPE, CONTINUE_ACTION_TYPE
from pictor.utils.redis_helpers import write_json_to_cache, read_json_from_cache
from pictor.utils.analysis_helpers import task_avg_time, start_analysis, stop_analysis, reset_analysis, \
    continue_run_analysis, get_analysis_status, get_analysis_results, get_analysis_logs
from pictor.tasks.analysis_tasks import analysis_module_install_task


class AnalysisModuleViewSet(viewsets.ModelViewSet):
    """
    分析模块管理
    增刪改查，安裝/卸載
    """
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('name', 'version',)
    ordering_fields = '__all__'
    queryset = AnalysisModule.objects.order_by('-id').all()
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        name = request.data.get('name', '')
        version = request.data.get('version', '')
        if AnalysisModule.objects.filter(name=name, version=version).first():
            result = {'success': False, 'messages': '分析模块:{}@{} 已经存在, 不能重复创建'.format(name, version)}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = AnalysisModule.objects.get(pk=int(serializer.data['id']))
        action_log(request=request, user=request.user, action_type=CREATE_ACTION_TYPE, old_instance=None,
                   instance=instance, action_info=f'创建分析模块:{instance.name}@{instance.version}!')
        result = {'success': True, 'messages': f'创建分析模块:{instance.name}@{instance.version}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = {'success': True, 'messages': f'获取分析模块:{instance.name}@{instance.version}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_instance = self.get_object()
        name = request.data.get('name', '')
        version = request.data.get('version', '')
        if name != instance.name or version != instance.version:
            if AnalysisModule.objects.filter(name=name, version=version).first():
                result = {'success': False, 'messages': f'分析模块:{instance.name}@{instance.version} 已经存在, 不能修改'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        action_log(request=request, user=request.user, action_type=UPDATE_ACTION_TYPE, old_instance=instance,
                   instance=old_instance, action_info=f'修改分析模块:{instance.name}@{instance.version}!')
        result = {'success': True, 'messages': f'修改分析模块:{instance.name}@{instance.version}!',
                  'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        query_params = self.request.query_params
        not_page = query_params.get('not_page', False)
        queryset = self.filter_queryset(self.get_queryset())
        if not_page and not_page.lower() != 'false':
            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '成功获取分析模块不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '成功获取分析模块不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        action_log(request=request, user=request.user, action_type=DELETE_ACTION_TYPE, old_instance=None,
                   instance=None, action_info=f'删除分析模块:{instance.name}@{instance.version}!')
        result = {'success': True, 'messages': f'删除分析模块:{instance.name}@{instance.version}!'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=False)
    def bulk_delete(self, request, *args, **kwargs):
        """批量删除"""
        deleted_objects_ids = request.data.get('deleted_objects', [])
        queryset = self.get_queryset()
        deleted_objects = queryset.filter(id__in=deleted_objects_ids).all()
        deleted_objects_names = [deleted_object.__str__() for deleted_object in deleted_objects]
        deleted_objects.delete()
        action_log(request=request, user=request.user, action_type=BULK_DELETE_ACTION_TYPE, old_instance=None,
                   instance=None, action_info=f'批量删除分析模块:{deleted_objects_names}')
        result = {'success': True, 'messages': f'批量删除分析模块!'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def module_types(self, request, *args, **kwargs):
        results = [{"key": key, "value": value} for key, value in ANALYSIS_MODULE_TYPE.items()]
        result = {'success': True, 'messages': f'获取分析模块类型!', 'results': results}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def module_status(self, request, *args, **kwargs):
        results = [{"key": key, "value": value} for key, value in ANALYSIS_MODULE_STATUS.items()]
        result = {'success': True, 'messages': f'获取分析模块状态!', 'results': results}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def versions(self, request, *args, **kwargs):
        module_url = request.data.get('module_url', [])
        return_heads = read_json_from_cache(f'heads@{module_url}')
        return_tags = read_json_from_cache(f'tags@{module_url}')
        try:
            if not return_heads:
                return_heads = []
                full_heads = git.cmd.Git().ls_remote("--heads", module_url).split('\n')
                for full_head in full_heads:
                    if full_head:
                        return_heads.append(full_head.split('\t')[-1])
            if not return_tags:
                return_tags = []
                full_tags = git.cmd.Git().ls_remote("--tags", module_url).split('\n')
                for full_tag in full_tags:
                    if full_tag:
                        return_tags.append(full_tag.split('\t')[-1])
        except Exception as error:
            result = {'success': False, 'messages': f'无法获取链接对应的版本信息, 请检查URL是否正确:{error}!'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return_versions = []
        if return_tags:
            return_versions.extend(return_tags)
            write_json_to_cache(key=f'tags@{module_url}', value=return_tags, expire=60*60*24)
        if return_heads:
            return_versions.extend(return_heads)
            write_json_to_cache(key=f'heads@{module_url}', value=return_heads, expire=60*60*24)
        result = {'success': True, 'messages': f'成功获取:{module_url}的分支与标签号!', 'results': return_versions}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def install(self, request, *args, **kwargs):
        instance = self.get_object()
        analysis_module_install_task.delay(instance.id)
        instance.status = MODULE_DOING
        instance.save()
        result = {'success': True, 'messages': f'已启动模块安装, 请等待安装完毕'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def uninstall(self, request, *args, **kwargs):
        instance = self.get_object()
        file_path = instance.file_path
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
        instance.status = MODULE_UN_ACTIVE
        instance.save()
        result = {'success': True, 'messages': f'已卸载模块'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def stop_install(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = MODULE_UN_DONE
        instance.save()
        result = {'success': True, 'messages': f'已停止安装模块'}
        return Response(result, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return AnalysisModuleActionSerializer
        if self.action == 'retrieve':
            return AnalysisModuleDetailSerializer
        return AnalysisModuleListSerializer


class AnalysisParameterViewSet(viewsets.ModelViewSet):
    """
    分析参数， 增删改查
    """
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('module__name', 'module__version', 'name')
    ordering_fields = '__all__'
    queryset = AnalysisParameter.objects.order_by('-id').all()
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        name = request.data.get('name', '')
        module_id = request.data.get('module', '')
        try:
            module = AnalysisModule.objects.get(pk=int(module_id))
        except:
            module = None
        if AnalysisParameter.objects.filter(name=name, module=module).first():
            result = {'success': False, 'messages': f'分析参数:{name}已经存在, 不能重复创建'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = AnalysisParameter.objects.get(pk=int(serializer.data['id']))
        action_log(request=request, user=request.user, action_type=CREATE_ACTION_TYPE, old_instance=None,
                   instance=instance, action_info=f'新增分析参数:{instance.__str__()}')
        result = {'success': True, 'messages': f'新增分析参数:{instance.__str__()}', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = {'success': True, 'messages': f'获取分析参数:{instance.__str__()}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_instance = self.get_object()
        name = request.data.get('name', '')
        module_id = request.data.get('module', '')
        try:
            module = AnalysisModule.objects.get(pk=int(module_id))
        except:
            module = None
        if name != instance.name or module != instance.module:
            if AnalysisParameter.objects.filter(name=name, module=module).first():
                result = {'success': False, 'messages': f'分析参数:{instance.name}已经存在, 不能修改'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        action_log(request=request, user=request.user, action_type=CREATE_ACTION_TYPE, old_instance=old_instance,
                   instance=instance, action_info=f'修改分析参数:{instance.__str__()}')
        result = {'success': True, 'messages': f'修改分析参数:{instance.__str__()}',
                  'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        query_params = self.request.query_params
        not_page = query_params.get('not_page', False)
        module_id = query_params.get('module', False)
        queryset = self.filter_queryset(self.get_queryset())
        if module_id:
            module = AnalysisModule.objects.get(pk=int(module_id))
            queryset = queryset.filter(module=module)
        queryset = queryset.distinct()
        if not_page and not_page.lower() != 'false':
            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '获取分析参数不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '获取分析参数不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        result = {'success': True, 'messages': f'删除分析参数:{instance.__str__()}!'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=False)
    def bulk_delete(self, request, *args, **kwargs):
        """批量删除"""
        deleted_objects_ids = request.data.get('deleted_objects', [])
        queryset = self.get_queryset()
        deleted_objects = queryset.filter(id__in=deleted_objects_ids).all()
        deleted_objects_names = [f'{deleted_object.__str__()}' for deleted_object in deleted_objects]
        deleted_objects.delete()
        action_log(request=request, user=request.user, action_type=BULK_DELETE_ACTION_TYPE, old_instance=None,
                   instance=None, action_info=f'批量删除分析参数:{deleted_objects_names}')
        result = {'success': True, 'messages': f'批量删除分析参数!'}
        return Response(result, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return AnalysisParameterActionSerializer
        if self.action == 'retrieve':
            return AnalysisParameterDetailSerializer
        return AnalysisParameterListSerializer


class AnalysisViewSet(viewsets.ModelViewSet):
    """分析任务"""
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('serial_number', 'analysis_module__name', 'analysis_module__version')
    ordering_fields = ('serial_number',)
    queryset = Analysis.objects.order_by('-id').all()
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serial_number = request.data.get('serial_number', '')
        if Analysis.objects.filter(serial_number=serial_number).first():
            result = {'success': False, 'messages': f'分析任务:{serial_number} 已经存在, 不能重复创建'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = Analysis.objects.get(pk=int(serializer.data['id']))
        action_log(request=request, user=request.user, action_type=CREATE_ACTION_TYPE, old_instance=None,
                   instance=instance, action_info=f'新增分析任务:{instance.__str__()}')
        result = {'success': True, 'messages': f'新增分析任务:{instance.__str__()}', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = {'success': True, 'messages': f'获取分析任务:{instance.__str__()}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_instance = self.get_object()
        serial_number = request.data.get('serial_number', '')
        if serial_number != instance.serial_number and Analysis.objects.filter(serial_number=serial_number).first():
            result = {'success': False, 'messages': f'分析任务:{instance.serial_number} 已经存在, 不能修改'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        action_log(request=request, user=request.user, action_type=UPDATE_ACTION_TYPE, old_instance=old_instance,
                   instance=instance, action_info=f'修改分析任务:{instance.__str__()}')
        result = {'success': True, 'messages': f'修改分析任务:{instance.__str__()}',
                  'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        query_params = self.request.query_params
        not_page = query_params.get('not_page', False)
        work_zone_id = query_params.get('work_zone', False)
        api_logger.debug(f'{work_zone_id}')
        analysis_status = query_params.get('status', False)
        project_id = query_params.get('project', False)
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        queryset = self.filter_queryset(self.get_queryset())
        api_logger.debug(f'{work_zone}')
        if work_zone:
            queryset = queryset.filter(work_zone=work_zone)
        if analysis_status:
            queryset = queryset.filter(status=analysis_status)
        if project_id:
            project = Project.objects.get(pk=int(project_id))
            queryset = queryset.filter(project=project)
        queryset = queryset.distinct()
        if not_page and not_page.lower() != 'false':
            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '获取分析任务不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '获取分析任务不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        result = {'success': True, 'messages': f'删除分析任务:{instance.__str__()}!'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=False)
    def bulk_delete(self, request, *args, **kwargs):
        """批量删除"""
        deleted_objects_ids = request.data.get('deleted_objects', [])
        queryset = self.get_queryset()
        deleted_objects = queryset.filter(id__in=deleted_objects_ids).all()
        deleted_objects_names = [f'{deleted_object.__str__()}' for deleted_object in deleted_objects]
        deleted_objects.delete()
        action_log(request=request, user=request.user, action_type=BULK_DELETE_ACTION_TYPE, old_instance=None,
                   instance=None, action_info=f'批量删除分析:{deleted_objects_names}')
        result = {'success': True, 'messages': f'批量删除分析!'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def analysis_status(self, request, *args, **kwargs):
        """获取所有分析状态"""
        result = {'success': True, 'messages': f'批量删除分析!', 'results': ANALYSIS_STATUS}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def statistics(self, request, *args, **kwargs):
        query_params = self.request.query_params
        work_zone_id = query_params.get('work_zone', False)
        try:
            work_zone = WorkZone.ordering.get(pk=int(work_zone_id))
        except:
            work_zone = None
        queryset = self.filter_queryset(self.get_queryset())
        if work_zone:
            queryset = queryset.filter(work_zone=work_zone)
        total = queryset.distinct().count()
        month = datetime.now().strftime('%Y-%m')
        month_success_count = queryset.filter(created_time__startswith=month,
                                              status=ANALYSIS_SUCCESS).distinct().count()
        month_avg_time = task_avg_time(queryset.filter(created_time__startswith=month).distinct())
        results = [{'key': '总任务数', 'value': total}, {'key': '本月完成任务数', 'value': month_success_count},
                   {'key': '本月任务平均处理时间', 'value': f'{month_avg_time}分钟'}]
        result = {'success': True, 'messages': f'当前统计信息!',
                  'results': results}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def start(self, request, *args, **kwargs):
        # 启动分析任务
        instance = self.get_object()
        is_success, code, messages, resp_results = start_analysis(instance)
        if is_success:
            instance.status = ANALYSIS_RUNNING
            instance.started_time = datetime.now()
            instance.finished_time = None
            instance.save()
            result = {'success': True, 'messages': f'启动分析任务成功'}
            action_log(request=request, user=request.user, action_type=START_ACTION_TYPE, old_instance=instance,
                       instance=instance, action_info=f'启动分析任务:{instance.__str__()}')
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {'success': False, 'messages': f'启动分析任务发生错误, 返回码:{code},'
                                                    f' 错误信息:{messages}, 返回结果:{resp_results}'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def stop(self, request, *args, **kwargs):
        # 停止分析任务
        instance = self.get_object()
        is_success, code, messages, resp_results = stop_analysis(instance)
        if is_success:
            instance.status = ANALYSIS_STOP
            instance.finished_time = datetime.now()
            instance.save()
            result = {'success': True, 'messages': f'停止分析任务成功'}
            action_log(request=request, user=request.user, action_type=STOP_ACTION_TYPE, old_instance=instance,
                       instance=instance, action_info=f'停止分析任务:{instance.__str__()}')
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {'success': False, 'messages': f'停止分析任务发生错误, 返回码:{code},'
                                                    f' 错误信息:{messages}, 返回结果:{resp_results}'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def continue_run(self, request, *args, **kwargs):
        # 继续运行分析任务
        instance = self.get_object()
        is_success, code, messages, resp_results = continue_run_analysis(instance)
        if is_success:
            instance.status = ANALYSIS_RUNNING
            instance.finished_time = None
            instance.save()
            result = {'success': True, 'messages': f'继续运行分析任务成功'}
            action_log(request=request, user=request.user, action_type=CONTINUE_ACTION_TYPE, old_instance=instance,
                       instance=instance, action_info=f'继续运行分析任务:{instance.__str__()}')
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {'success': False, 'messages': f'继续运行分析任务发生错误, 返回码:{code},'
                                                    f' 错误信息:{messages}, 返回结果:{resp_results}'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def reset(self, request, *args, **kwargs):
        # 重置分析任务
        instance = self.get_object()
        is_success, code, messages, resp_results = reset_analysis(instance)
        if is_success:
            instance.status = ANALYSIS_RESET
            instance.save()
            result = {'success': True, 'messages': f'重置分析任务成功'}
            action_log(request=request, user=request.user, action_type=RESET_ACTION_TYPE, old_instance=instance,
                       instance=instance, action_info=f'重置分析任务:{instance.__str__()}')
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {'success': False, 'messages': f'重置分析任务发生错误, 返回码:{code},'
                                                    f' 错误信息:{messages}, 返回结果:{resp_results}'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True)
    def results(self, request, *args, **kwargs):
        # 重置分析任务
        instance = self.get_object()
        is_success, code, messages, resp_results = get_analysis_results(instance)
        if is_success:
            result = {'success': True, 'messages': f'获取分析任务结果', 'results': resp_results}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {'success': False, 'messages': f'获取分析任务结果发生错误, 返回码:{code},'
                                                    f' 错误信息:{messages}, 返回结果:{resp_results}'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True)
    def logs(self, request, *args, **kwargs):
        instance = self.get_object()
        is_success, code, messages, resp_results = get_analysis_logs(instance)
        if is_success:
            result = {'success': True, 'messages': f'获取分析任务日志', 'results': resp_results}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {'success': False, 'messages': f'获取分析任务日志发生错误, 返回码:{code},'
                                                    f' 错误信息:{messages}, 返回结果:{resp_results}'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return AnalysisActionSerializer
        if self.action == 'retrieve':
            return AnalysisDetailSerializer
        return AnalysisListSerializer
