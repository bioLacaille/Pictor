from rest_framework import viewsets, mixins, filters, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from pictor.models import AnalysisModule, AnalysisParameter
from pictor.serializers.analysis_serializers import AnalysisParameterDetailSerializer, AnalysisParameterActionSerializer, \
    AnalysisParameterListSerializer
from pictor.utils.applog_helpers import api_logger
from pictor.utils.actionlog_helpers import action_log
from pictor.configures import CREATE_ACTION_TYPE, BULK_DELETE_ACTION_TYPE


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