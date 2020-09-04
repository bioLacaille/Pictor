from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework import status
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework.response import Response
from pictor.models import User
from django.contrib.auth import authenticate
from pictor.utils.auth_helpers import get_jwt_token, jwt_response_payload_handler
from pictor.utils.applog_helpers import api_logger
from pictor.utils.actionlog_helpers import action_log
from pictor.configures import AUTH_ACTION_TYPE


class Authentication(JSONWebTokenAPIView):
    """
    Web端认证用户(帐号密码)
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username:
            result = {'success': False, 'messages': '用户帐号名必须存在, 请发送用户名!'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            result = {'success': False, 'messages': '密码必须存在, 请发送密码!'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(username=username).first()
        if user:
            if not user.is_active or user.is_deleted:
                result = {'success': False, 'messages': '当前用户已禁用或删除, 请使用其他用户!'}
                return Response(result, status=status.HTTP_403_FORBIDDEN)
            login_user = authenticate(username=username.strip(), password=password)
            if login_user is None:
                result = {'success': False, 'messages': '用户名:{}密码错误, 请输入正确密码!'.format(username)}
                return Response(result, status=status.HTTP_403_FORBIDDEN)
        else:
            result = {'success': False, 'messages': '用户名:{}不存在或无效, 请输入正确用户!'.format(username)}
            return Response(result, status=status.HTTP_403_FORBIDDEN)
        # 认证成功
        token = get_jwt_token(login_user)
        response_data = jwt_response_payload_handler(token, login_user, request)
        response = Response(response_data, status=status.HTTP_200_OK)
        # 操作日志记录
        api_logger.debug(f'{login_user}登录系统')
        action_log(request=request, user=login_user, action_type=AUTH_ACTION_TYPE, old_instance=None,
                   instance=login_user, action_info=f'使用账号密码登录系统')
        return response
    serializer_class = JSONWebTokenSerializer
