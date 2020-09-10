"""
Author: Alan Fu
Email: fualan1990@gmail.com
分析模块API接口
"""
from rest_framework import viewsets, mixins, filters, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from pictor.models import AnalysisModule
from pictor.serializers.analysis_serializers import AnalysisModuleActionSerializer, AnalysisModuleListSerializer, \
    AnalysisModuleDetailSerializer
import git
import os
import shutil
from pictor.utils.applog_helpers import api_logger
from pictor.utils.actionlog_helpers import action_log
from pictor.configures import CREATE_ACTION_TYPE, UPDATE_ACTION_TYPE, DELETE_ACTION_TYPE,  BULK_DELETE_ACTION_TYPE, \
    ANALYSIS_MODULE_TYPE, ANALYSIS_MODULE_STATUS,  MODULE_DOING, MODULE_UN_ACTIVE, MODULE_UN_DONE
from pictor.utils.redis_helpers import write_json_to_cache, read_json_from_cache
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