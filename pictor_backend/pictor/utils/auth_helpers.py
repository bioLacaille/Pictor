"""
Author: Alan Fu
api认证工具方法
"""
from rest_framework import pagination
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import get_username
from rest_framework_jwt.compat import get_username_field
import warnings
from datetime import datetime
import uuid
from calendar import timegm
from pictor.configures import ADMIN, ZONE_ADMIN, ZONE_MAINTAINER, ZONE_USER
from pictor.models import WorkZone, WorkZoneMember


class CustomPagination(pagination.PageNumberPagination):
    """自定义分页格式"""
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'success': True,
            'messages': '获取分页数据成功！',
            'all_count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })


def jwt_response_payload_handler(token, user=None, request=None, impersonated_by=None):
    """自定义授权返回"""

    result = {
        'success': True,
        'messages': "认证成功!使用帐号密码登录系统!",
        'results': {
            'token': token,
            'user': {'id': user.id, 'username': user.username, 'email': user.email,
                     'nickname': user.nickname, 'role': user.role},
        }
    }
    return result


def custom_exception_handler(exc, context):
    """自定义错误返回"""
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    try:
        # Now add the HTTP status code to the response.
        if response.data.get('detail', None):
            if response.data.get('detail', None).code == 'permission_denied':
                result = {'success': False, 'messages': f'当前用户没有权限操作, 请确认用户的工作区角色或系统角色',
                          'results': response.data}
                return Response(result, status=response.status_code)
            else:
                result = {'success': False, 'messages': '发生错误:{}'.format(response.data['detail']),
                          'results': response.data}
                return Response(result, status=response.status_code)
        else:
            result = {'success': False, 'messages': '发生错误:{}'.format(response.data),
                      'results': response.data}
            return Response(result, status=response.status_code)
    except:
        try:
            result = {'success': False, 'messages': '发生错误:{}'.format(response.data),
                      'results': response.data}
            return Response(result, status=response.status_code)
        except:
            return response


def jwt_payload_handler(user):
    """自定义jwt_payload_handler, 生成token的必要参数"""
    username_field = get_username_field()
    username = get_username(user)
    warnings.warn(
        'The following fields will be removed in the future: '
        '`email` and `user_id`. ',
        DeprecationWarning
    )
    payload = {
        'user_id': user.pk,
        'username': username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
    if hasattr(user, 'email'):
        payload['email'] = user.email
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)
    payload[username_field] = username
    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )
    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE
    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER
    return payload


def get_jwt_token(user):
    """换取token"""
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


class IsWorkZoneAdminForWorZone(BasePermission):
    # 检查是否工作区管理员或是否系统管理员
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if user.role_level >= ADMIN:
            return True
        work_zone_id = view.kwargs.get('pk', None)
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        if work_zone:
            work_zone_member = WorkZoneMember.objects.filter(work_zone=work_zone, user=request.user).first()
            if not work_zone_member:
                return False
            else:
                if work_zone_member.level != ZONE_ADMIN:
                    return False
                else:
                    return True
        else:
            return False


class IsWorkZoneAdmin(BasePermission):
    # 检查是否工作区管理员或是否系统管理员
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if user.role_level >= ADMIN:
            return True
        work_zone_id = request.data.get('work_zone', None)
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        if work_zone:
            work_zone_member = WorkZoneMember.objects.filter(work_zone=work_zone, user=request.user).first()
            if not work_zone_member:
                return False
            else:
                if work_zone_member.level < ZONE_ADMIN:
                    return False
                else:
                    return True
        else:
            return False


class IsWorkZoneMaintainer(BasePermission):
    # 检查是否工作区超级成员
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if user.role_level >= ADMIN:
            return True
        work_zone_id = request.data.get('work_zone', None)
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        if work_zone:
            work_zone_member = WorkZoneMember.objects.filter(work_zone=work_zone, user=request.user).first()
            if not work_zone_member:
                return False
            else:
                if work_zone_member.level < ZONE_MAINTAINER:
                    return False
                else:
                    return True
        else:
            return False


class IsWorkZoneUser(BasePermission):
    # 检查是否工作区成员
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if user.role_level >= ADMIN:
            return True
        work_zone_id = request.data.get('work_zone', None)
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        if work_zone:
            work_zone_member = WorkZoneMember.objects.filter(work_zone=work_zone, user=request.user).first()
            if not work_zone_member:
                return False
            else:
                if work_zone_member.level < ZONE_USER:
                    return False
                else:
                    return True
        else:
            return False


class IsAdmin(BasePermission):
    # 检查是否工作区管理员或是否系统管理员
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if user.role_level >= ADMIN:
            return True
        else:
            return False