from rest_framework import viewsets, mixins, filters, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from pictor.models import Sample, DataSet, WorkZone, Project
from django.db.models import Count
from pictor.utils.applog_helpers import api_logger
from pictor.utils.actionlog_helpers import action_log
from pictor.configures import CREATE_ACTION_TYPE, UPDATE_ACTION_TYPE, DELETE_ACTION_TYPE, BULK_DELETE_ACTION_TYPE
from pictor.utils.dataset_helpers import get_data_files
from pictor.serializers.sample_serializers import SampleListSerializer, SampleDetailSerializer, SampleActionSerializer
from pictor.serializers.dataset_serializers import DataSetListSerializer
from pictor.utils.auth_helpers import IsWorkZoneAdmin, IsWorkZoneMaintainer, IsWorkZoneUser


class SampleViewSet(viewsets.ModelViewSet):
    """样本"""
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('serial_number', 'sample_name', 'sample_type', 'sample_source',)
    ordering_fields = ('serial_number', 'sample_name', 'sample_type', 'sample_source',)
    queryset = Sample.objects.order_by('-id').all()

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update':
            return [permissions.IsAuthenticated(), IsWorkZoneUser()]
        if self.action == 'destroy':
            return [permissions.IsAuthenticated(), IsWorkZoneMaintainer()]
        return [permissions.IsAuthenticated(), ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serial_number = request.data.get('serial_number', '')
        if Sample.objects.filter(serial_number=serial_number).first():
            result = {'success': False, 'messages': f'样本:{serial_number} 已经存在, 不能重复创建'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = Sample.objects.get(pk=int(serializer.data['id']))
        action_log(request=request, user=request.user, action_type=CREATE_ACTION_TYPE, old_instance=None,
                   instance=instance, action_info=f'新增样本:{instance.__str__()}')
        result = {'success': True, 'messages': f'新增样本:{instance.__str__()}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = {'success': True, 'messages': f'获取样本信息:{instance.__str__()}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_instance = self.get_object()
        serial_number = request.data.get('serial_number', '')
        if serial_number != instance.serial_number and Sample.objects.filter(serial_number=serial_number).first():
            result = {'success': False, 'messages': f'样本编号:{instance.__str__()} 已经存在, 不能修改成此编号'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        action_log(request=request, user=request.user, action_type=UPDATE_ACTION_TYPE, old_instance=old_instance,
                   instance=instance, action_info=f'修改样本:{instance.__str__()}')
        result = {'success': True, 'messages': f'修改样本:{instance.__str__()}!',
                  'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        query_params = self.request.query_params
        not_page = query_params.get('not_page', False)
        valid = query_params.get('valid', False)  # 有效样本, 即已经关联文件数据的样本
        work_zone_id = query_params.get('work_zone', False)
        project_id = query_params.get('project', False)
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        queryset = self.filter_queryset(self.get_queryset())
        if valid:
            queryset = queryset.annotate(dataset_count=Count('dataset')).filter(dataset_count__gt=0)
        if work_zone:
            queryset = queryset.filter(work_zone=work_zone)
        if project_id:
            project = Project.objects.get(pk=int(project_id))
            queryset = queryset.filter(project=project)
        queryset = queryset.distinct()
        if not_page and not_page.lower() != 'false':
            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '获取样本不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '获取样本不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        action_log(request=request, user=request.user, action_type=DELETE_ACTION_TYPE, old_instance=None,
                   instance=None, action_info=f'删除样本:{instance.__str__()}')
        result = {'success': True, 'messages': f'删除样本:{instance.__str__()}'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=False)
    def bulk_delete(self, request, *args, **kwargs):
        # 批量删除
        deleted_objects_ids = request.data.get('deleted_objects', [])
        queryset = self.get_queryset()
        deleted_objects = queryset.filter(id__in=deleted_objects_ids).all()
        deleted_objects_names = [f'{deleted_object.__str__()}' for deleted_object in deleted_objects]
        deleted_objects.delete()
        action_log(request=request, user=request.user, action_type=BULK_DELETE_ACTION_TYPE, old_instance=None,
                   instance=None, action_info=f'批量删除样本:{deleted_objects_names}')
        result = {'success': True, 'messages': f'批量删除样本!'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post', 'get'], detail=True)
    def related_dataset(self, request, *args, **kwargs):
        """关联文件数据"""
        instance = self.get_object()
        if request.method == 'GET':
            dataset = instance.dataset.all()
            data_files = DataSetListSerializer(dataset, many=True).data
            result = {'success': True, 'messages': f'成功样本:{instance.serial_number}的文件信息', 'results': data_files}
            return Response(result, status=status.HTTP_200_OK)
        else:
            data_id = request.data.get('data_id', '')
            if not data_id:
                result = {'success': False, 'messages': f'请选择文件数据!'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            related_files = []
            instance.dataset.clear()
            if isinstance(data_id, list):
                for d_id in data_id:
                    dataset = DataSet.objects.get(pk=int(d_id))
                    instance.dataset.add(dataset)
                    related_files.append(dataset.file_name)
            else:
                dataset = DataSet.objects.get(pk=int(data_id))
                instance.related_files.add(dataset)
                related_files.append(dataset.file_name)
            messages = f'样本:{instance.__str__()}关联文件数据:{related_files}'
            action_log(request=request, user=request.user, action_type=UPDATE_ACTION_TYPE, old_instance=instance,
                       instance=instance, action_info=messages)
            result = {'success': True, 'messages': messages}
            return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def all_related_files(self, request, *args, **kwargs):
        # 获取多选样本的关联文件数据
        sample_ids = request.data.get('sample_ids', [])
        dataset = []
        for sample_id in sample_ids:
            sample = Sample.objects.get(pk=int(sample_id))
            dataset.extend(sample.related_files.all())
        data_files = get_data_files(list(set(dataset)))
        result = {'success': True, 'messages': f'成功样本的文件信息', 'results': data_files}
        return Response(result, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return SampleActionSerializer
        if self.action == 'retrieve':
            return SampleDetailSerializer
        return SampleListSerializer
