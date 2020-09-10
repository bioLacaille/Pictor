"""
Author: Alan Fu
Email: fualan1990@gmail.com
操作权限API接口
"""
from rest_framework import viewsets, mixins, filters, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from pictor.models import WorkZone
from pictor.configures.permission_configures import *
from pictor.utils.permission_heplers import get_work_zone_permission, get_project_permission, get_sample_permission, \
    get_analysis_permission, get_dataset_permission, get_num_set_permission


class PermissionViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        query_params = self.request.query_params
        work_zone_id = query_params.get('work_zone', False)
        permission_type = query_params.get('permission_type', False)
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        if not permission_type:
            result = {'success': True, 'messages': '尚未指定查询类型, 返回默认权限', 'results': ACTION_PERMISSION}
            return Response(result, status=status.HTTP_200_OK)
        if permission_type == 'work_zone':
            work_zone_permission = get_work_zone_permission(user=request.user, work_zone=work_zone)
            result = {'success': True, 'messages': f'获取:{permission_type}的权限',
                      'results': {permission_type: work_zone_permission}}
        elif permission_type == 'project':
            project_permission = get_project_permission(user=request.user, work_zone=work_zone)
            result = {'success': True, 'messages': f'获取:{permission_type}的权限',
                      'results': {permission_type: project_permission}}
        elif permission_type == 'sample':
            sample_permission = get_sample_permission(user=request.user, work_zone=work_zone)
            result = {'success': True, 'messages': f'获取:{permission_type}的权限',
                      'results': {permission_type: sample_permission}}
        elif permission_type == 'dataset':
            dataset_permission = get_dataset_permission(user=request.user, work_zone=work_zone)
            result = {'success': True, 'messages': f'获取:{permission_type}的权限',
                      'results': {permission_type: dataset_permission}}
        elif permission_type == 'analysis':
            analysis_permission = get_analysis_permission(user=request.user, work_zone=work_zone)
            result = {'success': True, 'messages': f'获取:{permission_type}的权限',
                      'results': {permission_type: analysis_permission}}
        elif permission_type == 'setting':
            setting_permission = get_num_set_permission(user=request.user, work_zone=work_zone)
            result = {'success': True, 'messages': f'获取:{permission_type}的权限',
                      'results': {permission_type: setting_permission}}
        else:
            result = {'success': True, 'messages': '尚未指定查询类型, 返回默认权限', 'results': ACTION_PERMISSION}
        return Response(result, status=status.HTTP_200_OK)