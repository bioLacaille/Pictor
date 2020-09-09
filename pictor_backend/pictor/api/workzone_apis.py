"""
Author: Alan Fu
Email: fualan1990@gmail.com
工作区API接口
1.新增工作区
2.编辑工作区信息
3.获取工作区详情
4.工作区查询
5.获取/调整工作区成员
6.删除工作区
7.工作区成员类型
8.验证当前用户是否工作区成员
"""
from rest_framework import viewsets, mixins, filters, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from pictor.models import WorkZone, WorkZoneMember, User
from pictor.serializers.workzone_serializers import WorkZoneActionSerializer, WorkZoneDetailSerializer, \
    WorkZoneListSerializer, WorkZoneMemberBaseSerializer, UserBaseSerializer
from pictor.utils.applog_helpers import api_logger
from pictor.utils.actionlog_helpers import action_log
from pictor.configures import CREATE_ACTION_TYPE, UPDATE_ACTION_TYPE, DELETE_ACTION_TYPE, ZONE_ADMIN, \
    MEMBER_TYPE_ZH, MEMBER_TYPE, ADMIN


class WorkZoneViewSet(viewsets.ModelViewSet):
    """工作区"""
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('serial_number', 'name', 'remark')
    ordering_fields = ('serial_number', 'name', 'remark')
    queryset = WorkZone.objects.order_by('-id').all()
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        """新增工作区"""
        serializer = self.get_serializer(data=request.data)
        serial_number = request.data.get('serial_number', '')
        if WorkZone.objects.filter(serial_number=serial_number).first():
            result = {'success': False, 'messages': f'工作区:{serial_number} 已经存在, 编号可能已被其他用户未使用, 不能重复创建!'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = WorkZone.objects.get(pk=int(serializer.data['id']))
        action_log(request=request, user=request.user, action_type=CREATE_ACTION_TYPE, old_instance=None,
                   instance=instance, action_info=f'新增工作区:{instance.__str__()}')
        result = {'success': True, 'messages': f'新增工作区:{instance.__str__()}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK, headers=headers)

    def update(self, request, *args, **kwargs):
        """编辑工作区信息"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_instance = self.get_object()
        serial_number = request.data.get('serial_number', '')
        if serial_number != instance.serial_number and WorkZone.objects.filter(serial_number=serial_number).first():
            result = {'success': False, 'messages': f'工作区:{instance.__str__()} 已经存在, 不能修改成此编号'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        action_log(request=request, user=request.user, action_type=UPDATE_ACTION_TYPE, old_instance=old_instance,
                   instance=instance, action_info=f'修改工作区:{instance.__str__()}')
        result = {'success': True, 'messages': f'修改工作区:{instance.__str__()}',
                  'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """修改工作区信息"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """获取工作区详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = {'success': True, 'messages': f'获取工作区信息:{instance.__str__()}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """工作区查询"""
        query_params = self.request.query_params
        not_page = query_params.get('not_page', False)
        show_all = query_params.get('show_all', 'false')
        queryset = self.filter_queryset(self.get_queryset())
        show_all = True if show_all == 'true' else False
        if show_all:
            if request.user.role_level >= ADMIN:
                queryset = queryset
            else:
                queryset = queryset.filter(work_zone_members__user=request.user)
        else:
            queryset = queryset.filter(work_zone_members__user=request.user)
        queryset = queryset.distinct()
        if not_page and not_page.lower() != 'false':
            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '成功获取工作区不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '成功获取工作区不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """删除工作区"""
        instance = self.get_object()
        self.perform_destroy(instance)
        action_log(request=request, user=request.user, action_type=DELETE_ACTION_TYPE, old_instance=None,
                   instance=None, action_info=f'删除工作区:{instance.__str__()}')
        result = {'success': True, 'messages': f'删除工作区:{instance.__str__()}'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post', 'get'], detail=True)
    def members(self, request, *args, **kwargs):
        """获取/保存工作区成员"""
        instance = self.get_object()
        if request.method == 'GET':
            query_params = self.request.query_params
            filter_not_members = query_params.get('filter_not_members', False)
            if filter_not_members:
                user_ids = WorkZoneMember.objects.filter(work_zone=instance).values_list('user__id', flat=True).all()
                users = User.objects.exclude(id__in=user_ids, is_deleted=False, is_active=True).all()
                users = UserBaseSerializer(users, many=True).data
                result = {'success': True, 'messages': '成功获取工作区未选用户!',
                          'results': users}
                return Response(result, status=status.HTTP_200_OK)
            else:
                level = query_params.get('level', None)
                if not level:
                    all_members = WorkZoneMember.objects.filter(work_zone=instance).all()
                else:
                    all_members = WorkZoneMember.objects.filter(work_zone=instance, level=int(level)).all()
                all_members_data = WorkZoneMemberBaseSerializer(all_members, many=True).data
                result = {'success': True, 'messages': '成功获取工作区成员!',
                          'results': all_members_data}
                return Response(result, status=status.HTTP_200_OK)
        else:
            user_id = request.data.get('user', False)
            level = request.data.get('level', None)
            user = User.objects.get(pk=int(user_id))
            member = WorkZoneMember.objects.filter(work_zone=instance, user=user).first()
            if member:
                if not level:
                    member.delete()
                    action_log(request=request, user=request.user, action_type=UPDATE_ACTION_TYPE,
                               old_instance=instance,
                               instance=instance,
                               action_info=f'将工作区成员:{user.__str__()} 移出 {instance.__str__()}')
                    result = {'success': True,
                              'messages': f'将工作区成员:{user.__str__()} 移出 {instance.__str__()}'}
                    return Response(result, status=status.HTTP_200_OK)
                # 若调整工作区管理员, 需要确认当前是否仍存在工作区管理员
                if member.level == ZONE_ADMIN and int(level) != ZONE_ADMIN:
                    admin_member_count = WorkZoneMember.objects.filter(work_zone=instance, level=ZONE_ADMIN).count()
                    if admin_member_count <= 1:
                        result = {'success': False, 'messages': f'必须存在一个或以上的工作区管理员!', 'results': {}}
                        return Response(result, status=status.HTTP_400_BAD_REQUEST)
                member.level = level
                member.save()
            else:
                member = WorkZoneMember.objects.create(user=user, work_zone=instance, level=level)
            action_log(request=request, user=request.user, action_type=UPDATE_ACTION_TYPE, old_instance=instance,
                       instance=instance,
                       action_info=f'选择工作区成员:{user.__str__()} 为 {MEMBER_TYPE_ZH.get(int(level), int(level))}')
            serializer = WorkZoneMemberBaseSerializer(member)
            result = {'success': True,
                      'messages': f'选择工作区成员:{user.__str__()} 为 {MEMBER_TYPE_ZH.get(int(level), int(level))}',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def member_types(self, request, *args, **kwargs):
        """获取成员类型"""
        query_params = self.request.query_params
        zh = query_params.get('zh', '')
        mixing = query_params.get('mixing', '')
        if zh.lower() == 'true':
            result = {'success': True, 'messages': f'获取成员类型!', 'results': MEMBER_TYPE_ZH}
            return Response(result, status=status.HTTP_200_OK)
        if mixing.lower() == 'true':
            m_types = []
            for key, value in MEMBER_TYPE.items():
                m_types.append({'key': key, 'value': value, 'desc': MEMBER_TYPE_ZH.get(key)})
            result = {'success': True, 'messages': f'获取成员类型!', 'results': m_types}
            return Response(result, status=status.HTTP_200_OK)
        result = {'success': True, 'messages': f'获取成员类型!', 'results': MEMBER_TYPE}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def valid(self, request, *args, **kwargs):
        """验证当前用户是否工作区成员"""
        query_params = self.request.query_params
        work_zone_id = query_params.get('work_zone', False)
        api_logger.debug(f'获取work_zone_id:{work_zone_id}')
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        if work_zone:
            work_zone_member = WorkZoneMember.objects.filter(work_zone=work_zone, user=request.user).first()
            api_logger.debug(f'获取 work_zone_members:{work_zone_member}')
            if work_zone_member:
                result = {'success': True, 'messages': f'当前用户为该工作区成员!', 'results': {}}
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = {'success': False, 'messages': f'当前用户不是该工作区成员!', 'results': {}}
                return Response(result, status=status.HTTP_200_OK)
        else:
            result = {'success': False, 'messages': f'当前工作区获取错误!', 'results': {}}
            return Response(result, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return WorkZoneActionSerializer
        if self.action == 'retrieve':
            return WorkZoneDetailSerializer
        return WorkZoneListSerializer


