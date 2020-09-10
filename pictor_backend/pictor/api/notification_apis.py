"""
Author: Alan Fu
Email: fualan1990@gmail.com
站内信箱API接口
"""
from rest_framework import viewsets, filters, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import status
from pictor.models import Notification
from pictor.utils.applog_helpers import api_logger
from pictor.utils.actionlog_helpers import action_log
from pictor.configures import READ_NOTIFY_ACTION_TYPE, UNREAD_NOTIFY_ACTION_TYPE, DELETE_NOTIFY_ACTION_TYPE,\
    CLEAR_NOTIFY_ACTION_TYPE, RECOVER_NOTIFY_ACTION_TYPE
from pictor.serializers.notification_serializers import NotificationSerializer
from pictor.utils.notification_helpers import send_notify


class NotificationViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Notification.objects.order_by('-id').all()
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ('title', 'content', )
    ordering_fields = ('level', )
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = {'success': True, 'messages': f'成功获取站内消息:{instance.title}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        # 列表展示
        # send_notify(title='测试', content='测试内容', content_object=request.user, recipient=[request.user])
        not_page = self.request.query_params.get('not_page', False)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(recipient=request.user)
        if not_page and not_page.lower() != 'false':
            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': f'成功获取消息列表!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': f'成功获取消息列表!',
                      'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def mark(self, request, *args, **kwargs):
        # 单个标记
        mark = request.data.get('mark', None)
        old_instance = self.get_object()
        instance = self.get_object()
        # 标记动作，当前可选值为['unread', 'read', 'delete', 'recover', 'clear']
        if mark == 'unread':
            instance.mark_as_unread()
            action_flag = UNREAD_NOTIFY_ACTION_TYPE
            mark_desc = '未读'
        elif mark == 'read':
            instance.mark_as_read()
            action_flag = READ_NOTIFY_ACTION_TYPE
            mark_desc = '已读'
        elif mark == 'delete':
            instance.mark_as_deleted()
            action_flag = DELETE_NOTIFY_ACTION_TYPE
            mark_desc = '删除'
        elif mark == 'recover':
            instance.mark_as_active()
            action_flag = RECOVER_NOTIFY_ACTION_TYPE
            mark_desc = '恢复'
        elif mark == 'clear':
            old_instance = None
            instance.delete()
            action_flag = CLEAR_NOTIFY_ACTION_TYPE
            mark_desc = '清空'
        else:
            action_flag = None
            mark_desc = None
        if action_flag:
            action_log(request=request, user=request.user, action_type=action_flag, old_instance=old_instance,
                       instance=instance, action_info=f'{mark_desc}站内消息:{instance.title}')
            result = {'success': True, 'messages': f'{mark_desc}站内消息:{instance.title}'}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {'success': False, 'messages': f'参数mark错误!请标记为以下值:[unread, read, delete, recover, clear]',
                      'results': []}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def bulk_mark(self, request, *args, **kwargs):
        # 批量标记多个
        notification_ids = request.data.get('notifications', [])
        mark = request.data.get('mark', None)
        queryset = self.get_queryset()
        queryset = queryset.filter(id__in=[int(notification_id) for notification_id in notification_ids])
        # 标记动作，当前可选值为['unread', 'read', 'delete', 'recover', 'clear']
        if mark == 'unread':
            queryset.unread()
            action_flag = UNREAD_NOTIFY_ACTION_TYPE
            mark_desc = '未读'
        elif mark == 'read':
            queryset.read()
            action_flag = READ_NOTIFY_ACTION_TYPE
            mark_desc = '已读'
        elif mark == 'delete':
            queryset.deleted()
            action_flag = DELETE_NOTIFY_ACTION_TYPE
            mark_desc = '删除'
        elif mark == 'recover':
            queryset.active()
            action_flag = RECOVER_NOTIFY_ACTION_TYPE
            mark_desc = '恢复'
        elif mark == 'clear':
            queryset.delete()
            action_flag = CLEAR_NOTIFY_ACTION_TYPE
            mark_desc = '清空'
        else:
            action_flag = None
            mark_desc = None
        titles = [instance.title for instance in queryset]
        if action_flag:
            action_log(request=request, user=request.user, action_type=action_flag, old_instance=None,
                       instance=None, action_info=f'批量{mark_desc}站内消息:{titles}')
            result = {'success': True, 'messages': f'批量{mark_desc}站内消息:{titles}'}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {'success': False, 'messages': f'参数mark错误!请标记为以下值:[unread, read, delete, recover, clear]',
                      'results': []}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def all_mark(self, request, *args, **kwargs):
        # 全部标记
        mark = request.data.get('mark', None)
        queryset = self.get_queryset()
        # 标记动作，当前可选值为['unread', 'read', 'delete', 'recover', 'clear']
        if mark == 'unread':
            queryset.unread_all(recipient=request.user)
            action_flag = UNREAD_NOTIFY_ACTION_TYPE
            mark_desc = '未读'
        elif mark == 'read':
            queryset.read_all(recipient=request.user)
            action_flag = READ_NOTIFY_ACTION_TYPE
            mark_desc = '已读'
        elif mark == 'delete':
            queryset.delete_all(recipient=request.user)
            action_flag = DELETE_NOTIFY_ACTION_TYPE
            mark_desc = '删除'
        elif mark == 'recover':
            queryset.active_all(recipient=request.user)
            action_flag = RECOVER_NOTIFY_ACTION_TYPE
            mark_desc = '恢复'
        elif mark == 'clear':
            queryset.filter(recipient=request.user).delete()
            action_flag = CLEAR_NOTIFY_ACTION_TYPE
            mark_desc = '清空'
        else:
            action_flag = None
            mark_desc = None
        if action_flag:
            action_log(request=request, user=request.user, action_type=action_flag, old_instance=None,
                       instance=None, action_info=f'{mark_desc}所有站内消息')
            result = {'success': True, 'messages': f'{mark_desc}所有站内消息'}
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = {'success': False, 'messages': f'参数mark错误!请标记为以下值:[unread, read, delete, recover, clear]',
                      'results': []}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        return NotificationSerializer
