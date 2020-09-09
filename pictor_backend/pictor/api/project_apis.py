"""
Author: Alan Fu
Email: fualan1990@gmail.com
项目API接口
1.新增项目
2.编辑项目
3.获取项目详情
4.项目查询
5.删除/批量删除项目
6.项目统计信息
"""
from rest_framework import viewsets, mixins, filters, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from pictor.models import Project, WorkZone, Sample, Analysis
from pictor.utils.applog_helpers import api_logger
from pictor.utils.actionlog_helpers import action_log
from pictor.configures import CREATE_ACTION_TYPE, UPDATE_ACTION_TYPE, DELETE_ACTION_TYPE, BULK_DELETE_ACTION_TYPE, \
    ANALYSIS_SUCCESS
from pictor.serializers.project_serializers import ProjectActionSerializer, ProjectDetailSerializer
from datetime import datetime
from django.db.models import Count
from pictor.utils.analysis_helpers import task_avg_time


class ProjectViewSet(viewsets.ModelViewSet):
    """项目"""
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('name', 'serial_number')
    ordering_fields = ('work_zone__name', 'serial_number', 'name', 'remark', 'created_time')
    queryset = Project.objects.order_by('-id').all()
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        """新增项目"""
        serializer = self.get_serializer(data=request.data)
        serial_number = request.data.get('serial_number', '')
        if Project.objects.filter(serial_number=serial_number).first():
            result = {'success': False, 'messages': f'项目:{serial_number} 已经存在, 不能重复创建'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = Project.objects.get(pk=int(serializer.data['id']))
        action_log(request=request, user=request.user, action_type=CREATE_ACTION_TYPE, old_instance=None,
                   instance=instance, action_info=f'新增项目:{instance.__str__()}')
        result = {'success': True, 'messages': f'新增项目:{instance.__str__()}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        """获取项目详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = {'success': True, 'messages': f'获取项目信息:{instance.__str__()}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """编辑项目"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_instance = self.get_object()
        serial_number = request.data.get('serial_number', '')
        if serial_number != instance.serial_number and Project.objects.filter(serial_number=serial_number).first():
            result = {'success': False, 'messages': f'项目:{instance.__str__()} 已经存在, 不能修改成此编号'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        action_log(request=request, user=request.user, action_type=UPDATE_ACTION_TYPE, old_instance=old_instance,
                   instance=instance, action_info=f'修改项目:{instance.__str__()}')
        result = {'success': True, 'messages': f'修改项目:{instance.__str__()}',
                  'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """编辑项目"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """项目查询"""
        query_params = self.request.query_params
        not_page = query_params.get('not_page', False)
        work_zone_id = query_params.get('work_zone', False)
        queryset = self.filter_queryset(self.get_queryset())
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        if work_zone:
            queryset = queryset.filter(work_zone=work_zone)
        if not_page and not_page.lower() != 'false':
            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '成功获取项目不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '成功获取项目不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """删除项目"""
        instance = self.get_object()
        self.perform_destroy(instance)
        action_log(request=request, user=request.user, action_type=DELETE_ACTION_TYPE, old_instance=None,
                   instance=None, action_info=f'删除项目:{instance.__str__()}')
        result = {'success': True, 'messages': f'删除项目:{instance.__str__()}!'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=False)
    def bulk_delete(self, request, *args, **kwargs):
        """批量删除项目"""
        # 批量删除
        deleted_objects_ids = request.data.get('deleted_objects', [])
        queryset = self.get_queryset()
        deleted_objects = queryset.filter(id__in=deleted_objects_ids).all()
        deleted_objects_names = [f'{deleted_object.__str__()}' for deleted_object in deleted_objects]
        deleted_objects.delete()
        action_log(request=request, user=request.user, action_type=BULK_DELETE_ACTION_TYPE, old_instance=None,
                   instance=None, action_info=f'批量删除项目:{deleted_objects_names}')
        result = {'success': True, 'messages': f'批量删除项目!'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def statistics(self, request, *args, **kwargs):
        """项目统计信息"""
        instance = self.get_object()
        sample_queryset = Sample.objects.filter(project=instance)
        analysis_queryset = Analysis.objects.filter(project=instance)
        month = datetime.now().strftime('%Y-%m')
        sample_total = sample_queryset.count()
        valid_count = sample_queryset.annotate(dataset_count=Count('dataset')). \
            filter(dataset_count__gt=0).distinct().count()
        month_avg_count = sample_queryset.filter(created_time__startswith=month).distinct().count()
        analysis_total = analysis_queryset.distinct().count()
        analysis_month_success_count = analysis_queryset.filter(created_time__startswith=month,
                                                                status=ANALYSIS_SUCCESS).distinct().count()
        analysis_month_avg_time = task_avg_time(analysis_queryset.filter(created_time__startswith=month).distinct())
        sample_statistics = [{'key': '样本数', 'value': sample_total},
                             {'key': '已关联数据样本数', 'value': valid_count},
                             {'key': '本月新增样本数', 'value': month_avg_count},
                             ]
        analysis_statistics = [{'key': '总任务数', 'value': analysis_total},
                               {'key': '本月完成任务数', 'value': analysis_month_success_count},
                                   {'key': '本月任务平均处理时间', 'value': f'{analysis_month_avg_time}分钟'}]
        result = {'success': True, 'messages': f'当前统计信息!',
                  'results': {'sample_statistics': sample_statistics, 'analysis_statistics': analysis_statistics}}
        return Response(result, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectActionSerializer
