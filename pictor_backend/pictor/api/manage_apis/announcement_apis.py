"""
Author: Alan Fu
Email: fualan1990@gmail.com
公告管理API接口
"""
from rest_framework import viewsets, mixins, filters, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from pictor.models import Announcement
from pictor.utils.applog_helpers import api_logger
from pictor.utils.actionlog_helpers import action_log
from pictor.configures import CREATE_ACTION_TYPE, UPDATE_ACTION_TYPE, DELETE_ACTION_TYPE, BULK_DELETE_ACTION_TYPE, \
    ACTIVE_ACTION_TYPE, DISABLE_ACTION_TYPE
from pictor.serializers.manage_serializers import AnnouncementSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    公告管理, 增刪改查
    """
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('title', )
    ordering_fields = '__all__'
    queryset = Announcement.objects.order_by('-id').all()
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = Announcement.objects.get(pk=int(serializer.data['id']))
        # 操作日志记录
        action_log(request=request, user=request.user, action_type=CREATE_ACTION_TYPE, old_instance=None,
                   instance=instance, action_info=f'新增公告:{instance.__str__()}')
        result = {'success': True, 'messages': f'新增公告:{instance.__str__()}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = {'success': True, 'messages': f'获取公告信息:{instance.__str__()}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        # 操作日志记录
        action_log(request=request, user=request.user, action_type=UPDATE_ACTION_TYPE, old_instance=old_instance,
                   instance=instance, action_info=f'修改公告:{instance.__str__()}')
        result = {'success': True, 'messages': f'修改公告:{instance.__str__()}!',
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
            result = {'success': True, 'messages': '获取公告不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '获取公告不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # 操作日志记录
        action_log(request=request, user=request.user, action_type=DELETE_ACTION_TYPE, old_instance=None,
                   instance=None, action_info=f'刪除公告:{instance.__str__()}')
        result = {'success': True, 'messages': f'刪除公告:{instance.__str__()}'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=False)
    def bulk_delete(self, request, *args, **kwargs):
        """批量删除"""
        deleted_objects_ids = request.data.get('deleted_objects', [])
        queryset = self.get_queryset()
        deleted_objects = queryset.filter(id__in=deleted_objects_ids).all()
        messages = ','.join([deleted_object.__str__() for deleted_object in deleted_objects])
        deleted_objects.delete()
        # 操作日志记录
        action_log(request=request, user=request.user, action_type=BULK_DELETE_ACTION_TYPE, old_instance=None,
                   instance=None, action_info=f'批量删除公告:{messages}')
        result = {'success': True, 'messages': f'批量删除公告: {messages}!'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def publish(self, request, *args, **kwargs):
        """发布/下架"""
        old = self.get_object()
        instance = self.get_object()
        is_publish = request.data.get('publish', True)
        msg = '发布'
        action_type = ACTIVE_ACTION_TYPE
        if not is_publish:
            msg = '下架'
            action_type = DISABLE_ACTION_TYPE
        instance.is_publish = is_publish
        instance.save()
        # 操作日志记录
        action_log(request, request.user, action_type, old_instance=old, instance=instance,
                   action_info=f'{msg}公告:{instance.__str__()}')
        result = {'success': True, 'messages': f'{msg}公告:{instance.__str__()}'}
        return Response(result, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        return AnnouncementSerializer
