from rest_framework import mixins, viewsets, filters
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from pictor.configures.dataset_configures import *
from django.conf import settings
import os
import shutil
import glob
from pictor.utils.base_heplers import create_or_get_directory
from pictor.models import WorkZone, DataSet
from pictor.utils.dataset_helpers import get_data_directory_path, get_data_files, check_md5_sum
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db import transaction
from pictor.serializers.dataset_serializers import DataSetListSerializer, DataSetDetailSerializer, \
    DataSetActionSerializer
from pictor.utils.applog_helpers import api_logger
from pictor.utils.actionlog_helpers import action_log
from pictor.tasks import copy_move_dataset_task


class DataSetViewSet(viewsets.ModelViewSet):
    """文件数据"""
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('serial_number', 'directory_path', 'file_name', 'download_url',)
    ordering_fields = ('serial_number', 'directory_path', 'file_name', 'download_url',)
    queryset = DataSet.objects.order_by('-id').all()
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        result = {'success': False, 'messages': '该接口被禁用, 请勿发送请求！'}
        return Response(result, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = {'success': True, 'messages': f'获取文件信息:{instance.serial_number}!', 'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # 重命名
        instance = self.get_object()
        file_name = request.data.get('file_name', '')
        if not file_name:
            result = {'success': False, 'messages': '仅能修改文名称, 请输入文件名称！'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        if file_name != instance.file_name:
            file_path = instance.file_full_path
            new_file_path = os.path.join(os.path.dirname(file_path), file_name)
            if os.path.exists(new_file_path):
                result = {'success': False, 'messages': '该名称已存在于当前目录, 请勿修改成此名称！'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            os.rename(file_path, new_file_path)
        serializer = self.get_serializer(instance, data={'file_name': file_name}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        result = {'success': True, 'messages': '修改文件:{}!'.format(instance.file_name),
                  'results': serializer.data}
        return Response(result, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        # 文件列表
        query_params = self.request.query_params
        not_page = query_params.get('not_page', False)
        data_type = int(query_params.get('data_type', PUBLIC_DATA))
        file_type = query_params.get('file_type', None)
        work_zone_id = int(query_params.get('work_zone', 0))
        current_path = query_params.get('current_path', '')
        queryset = self.filter_queryset(self.get_queryset())
        if not data_type:
            result = {'success': False, 'messages': '无法确认当前所属文件类型！'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        queryset = queryset.filter(work_zone=work_zone, data_type=data_type,
                                   directory_path=current_path, uploaded=True)
        if file_type:
            queryset = queryset.filter(file_type=int(file_type))
        queryset = queryset.distinct()
        if not_page and not_page.lower() != 'false':
            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '获取项目不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)
        else:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            result = {'success': True, 'messages': '获取项目不分页数据!',
                      'results': serializer.data}
            return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=False)
    def bulk_delete(self, request, *args, **kwargs):
        # 批量删除
        deleted_objects_ids = request.data.get('deleted_objects', [])
        queryset = self.get_queryset()
        deleted_objects = queryset.filter(id__in=deleted_objects_ids).all()
        # 删除文件
        for deleted_object in deleted_objects:
            file_path = deleted_object.file_full_path
            if os.path.exists(file_path):
                if os.path.isfile(file_path):
                    os.remove(file_path)
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            self.perform_destroy(deleted_object)
        result = {'success': True, 'messages': f'成功批量删除文件!'}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def directory_path(self, request, *args, **kwargs):
        query_params = self.request.query_params
        data_type = int(query_params.get('data_type', 0))
        work_zone_id = int(query_params.get('work_zone', 0))
        valid = query_params.get('valid', False)
        query_path = query_params.get('query_path', '')
        if query_path.startswith('/'):
            query_path = query_path[1:]
        if query_path.endswith('/'):
            query_path = query_path[:-1]
        query_paths = query_path.rsplit('/', 1)
        if len(query_paths) == 2:
            parent_path, file_name = query_paths[0], query_paths[1]
        else:
            parent_path, file_name = '', query_path
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        if valid:
            if not parent_path and not file_name:
                result = {'success': True, 'messages': f'请求获取根目录'}
                return Response(result, status=status.HTTP_200_OK)
            dataset = DataSet.objects.filter(work_zone=work_zone, data_type=data_type,
                                             directory_path=parent_path, uploaded=True, file_type=20,
                                             file_name=file_name).first()
            if dataset:
                result = {'success': True, 'messages': '当前路径有效',
                          'results': os.path.join(dataset.directory_path, dataset.file_name)}
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = {'success': False, 'messages': f'当前路径无效:{query_path}'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            dataset = DataSet.objects.filter(work_zone=work_zone, data_type=data_type,
                                             directory_path=parent_path, uploaded=True, file_type=20,
                                             file_name__icontains=file_name).all()
            data_directory_path = []
            for data in dataset:
                data_directory_path.append({'key': data.id, 'value': os.path.join(data.directory_path, data.file_name)})
            result = {'success': True, 'messages': '成功获取当前路径下的文件夹路径', 'results': data_directory_path}
            return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def create_directory(self, request, *args, **kwargs):
        # 新增文件夹
        data_type = int(request.data.get('data_type', 0))
        current_path = request.data.get('current_path', '')
        work_zone_id = int(request.data.get('work_zone', 0))
        file_name = request.data.get('file_name', '')
        if not data_type:
            result = {'success': False, 'messages': '无法确认当前所属文件类型！'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        if not file_name:
            result = {'success': False, 'messages': '请输入文件夹名称！'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        data_path = get_data_directory_path(data_type=data_type, current_path=current_path, work_zone_id=work_zone_id)
        if not os.path.exists(data_path):
            result = {'success': False, 'messages': f'不存在当前路径:{data_path}！无法在该路径下创建文件夹'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        # 文件路路径
        directory_path = os.path.join(data_path, file_name)
        if os.path.exists(directory_path):
            result = {'success': False, 'messages': f'文件夹:{file_name}已经存在！请勿重复创建同名文件夹'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        os.makedirs(directory_path, exist_ok=True)
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        DataSet.objects.create(directory_path=current_path, file_name=file_name, data_type=data_type,
                               file_type=DIRECTORY, uploaded=True, work_zone=work_zone, creator=request.user)
        result = {'success': True, 'messages': f'成功创建文件夹:{file_name}', 'results': directory_path}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def data_types(self, request, *args, **kwargs):
        # 数据类型
        results = [{'key': key, 'value': value} for key, value in DATASET_TYPE_ZH.items()]
        result = {'success': True, 'messages': '成功获取数据类型', 'results': results}
        return Response(result, status=status.HTTP_200_OK)

    # @action(methods=['post'], detail=False)
    # def copy_move(self, request, *args, **kwargs):
    #     selected_dataset = request.data.get('dataset', [])
    #     data_type = int(request.data.get('data_type', 0))
    #     target_path = request.data.get('target_path', [])
    #     move = request.data.get('move', False)
    #     if not selected_dataset:
    #         result = {'success': False, 'messages': '请选择需要复制的文件/文件夹！'}
    #         return Response(result, status=status.HTTP_400_BAD_REQUEST)
    #     if not data_type:
    #         result = {'success': False, 'messages': '无法确认目标文件类型！'}
    #         return Response(result, status=status.HTTP_400_BAD_REQUEST)
    #     if not target_path:
    #         result = {'success': False, 'messages': '请指定目标路径！'}
    #         return Response(result, status=status.HTTP_400_BAD_REQUEST)
    #     copy_move_dataset_task.delay(selected_dataset, data_type, target_path, move)
    #     msg = '移动'
    #     if not move:
    #         msg = '复制'
    #     result = {'success': True, 'messages': f'已启动{msg}文件操作', 'results': {}}
    #     return Response(result, status=status.HTTP_200_OK)

    @action(methods=['post', 'get'], detail=False)
    def file_upload(self, request, *args, **kwargs):
        # 上传文件/大文件/断点续传
        # todo: 若前端进行并发请求, 将导致保存数据时出现BUG, 后续需要解决, 完善并发请求问题
        if request.method == 'GET':
            query_params = self.request.query_params
            data_type = int(query_params.get('data_type', PROJECT_DATA))
            current_path = query_params.get('current_path', '')
            work_zone_id = int(query_params.get('work_zone', None))
            try:
                work_zone = WorkZone.objects.get(pk=int(work_zone_id))
            except:
                work_zone = None
            if not data_type:
                result = {'success': False, 'messages': '无法确认当前所属文件类型！'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            chunk_index = query_params.get('chunk_index', None)  # 当前是第几个分片
            chunk_size = query_params.get('chunk_size', None)  # 每个分块大小
            current_chunk_size = query_params.get('current_chunk_size', None)  # 当前分块大小
            total_size = int(query_params.get('total_size', 0))  # 文件总大小
            file_md5 = query_params.get('file_md5', None)  # MD5
            file_name = query_params.get('file_name', None)  # 文件名称
            relative_path = query_params.get('relative_path', None)  # 关联路径
            total_chunks = int(query_params.get('total_chunks', 0))  # 分块总数
            if not file_md5:
                result = {'success': False, 'messages': '请指定文件MD5值'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            if not file_name:
                result = {'success': False, 'messages': '请指定文件名称:file_name'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            data_path = get_data_directory_path(data_type=data_type,
                                                current_path=current_path,
                                                work_zone_id=work_zone_id)
            file_path = os.path.join(data_path, file_name)
            save_directory = os.path.join(data_path, f'{file_md5}-part')
            # 若已经存在相同MD5文件, 但文件路径不一致, 将该文件复制到指定路径上, 并返回已上传标志, 实现秒传
            # 文件路径+文件MD5 一致, 即为完全相同的同一个文件,
            # 若文件存在, 即已经上传, 实现秒传
            # 若记录存在, 文件不存在, 即未上传完毕, 对比文件大小以及分块总数, 若对不上, 即分块有变化, 删除已有分块文件, 重新上传
            # 否则返回已上传分块
            saved_dataset = DataSet.objects.filter(file_md5=file_md5, uploaded=True).first()
            dataset = DataSet.objects.filter(data_type=data_type, work_zone=work_zone,
                                             directory_path=current_path, file_name=file_name, file_md5=file_md5).first()
            if saved_dataset and not dataset:
                api_logger.debug(f'已存在相同MD5数据, 目标路径不一样, 进行复制')
                create_or_get_directory(os.path.dirname(file_path))
                shutil.copyfile(saved_dataset.file_full_path, file_path)
                DataSet.objects.create(directory_path=current_path, file_name=file_name, data_type=data_type,
                                       file_type=FILE, file_size=total_size, uploaded=True, file_md5=file_md5,
                                       uploaded_chunks=saved_dataset.uploaded_chunks, total_chunks=total_chunks,
                                       work_zone=work_zone, creator=request.user)
                uploaded = True
                uploaded_chunks = saved_dataset.uploaded_chunks.split(',')
            else:
                if dataset:
                    if os.path.exists(file_path):
                        api_logger.debug(f'已存在文件路径与MD5一致的文件, uploaded_chunks:{dataset.uploaded_chunks}')
                        uploaded = True
                        uploaded_chunks = dataset.uploaded_chunks.split(',')
                    else:
                        if dataset.total_chunks != total_chunks or dataset.file_size != total_size:
                            api_logger.debug(f'存在记录, 但文件不存在, 且分块数与大小对不上')
                            uploaded = False
                            uploaded_chunks = []
                            if os.path.exists(file_path):
                                os.remove(file_path)
                            if os.path.exists(save_directory):
                                shutil.rmtree(save_directory)
                        else:
                            api_logger.debug(f'存在记录, 但文件不存在, 返回已记录上传的分块:{dataset.uploaded_chunks}')
                            uploaded = False
                            uploaded_chunks = dataset.uploaded_chunks.split(',')
                else:
                    api_logger.debug(f'不存在记录')
                    uploaded = False
                    uploaded_chunks = []
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    if os.path.exists(save_directory):
                        shutil.rmtree(save_directory)
            uploaded_chunks = [int(uploaded_chunk) for uploaded_chunk in uploaded_chunks if uploaded_chunk]
            # 确保重新上传最后分块， 触发合并操作
            if len(uploaded_chunks) >= 1:
                uploaded_chunks = uploaded_chunks[:-1]
            result = {'success': True, 'messages': f'当前文件:{file_name}的分块情况',
                      'results': {'file_path': file_path, 'file_name': file_name,
                                  'uploaded': uploaded,
                                  'uploaded_chunks': uploaded_chunks,
                                  }}
            return Response(result, status=status.HTTP_200_OK)
        else:
            data_type = int(request.data.get('data_type', 0))
            current_path = request.data.get('current_path', '')
            work_zone_id = int(request.data.get('work_zone', 0))
            try:
                work_zone = WorkZone.objects.get(pk=int(work_zone_id))
            except:
                work_zone = None
            if not data_type:
                result = {'success': False, 'messages': '无法确认当前所属文件类型！'}
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            chunk_index = request.data.get('chunk_index', None)  # 当前是第几个分片
            chunk_size = request.data.get('chunk_size', None)  # 每个分块大小
            current_chunk_size = request.data.get('current_chunk_size', None)  # 当前分块大小
            total_size = int(request.data.get('total_size', 0))  # 文件总大小
            file_md5 = request.data.get('file_md5', None)  # MD5
            file_name = request.data.get('file_name', None)  # 文件名称
            relative_path = request.data.get('relative_path', None)  # 关联路径
            total_chunks = int(request.data.get('total_chunks', 0))  # 分块总数
            chunk_file = request.data.get('file', None)  # 具体文件

            dataset = DataSet.objects.filter(data_type=data_type, work_zone=work_zone,
                                             directory_path=current_path, file_name=file_name, file_md5=file_md5).first()
            if not dataset:
                dataset = DataSet.objects.create(data_type=data_type, file_type=10, work_zone=work_zone, file_md5=file_md5,
                                                 directory_path=current_path, file_name=file_name,
                                                 file_size=total_size, total_chunks=total_chunks,
                                                 creator=request.user)
            save_directory = os.path.join(dataset.directory_full_path, f'{file_md5}-part')
            save_path = os.path.join(save_directory, f'{file_name}.part{chunk_index}')
            # 保存
            # default_storage不会覆盖文件, 若文件存在, 删除后重新上传
            if default_storage.exists(save_path):
                default_storage.delete(save_path)
            default_storage.save(save_path, ContentFile(chunk_file.read()))
            uploaded_chunks = dataset.uploaded_chunks
            api_logger.debug(f'当前分块:{chunk_index}')
            if uploaded_chunks:
                uploaded_chunks = set(uploaded_chunks.split(','))
                uploaded_chunks.add(chunk_index)
            else:
                uploaded_chunks = [chunk_index]
            api_logger.debug(f'保存后所有分块:{uploaded_chunks}')
            dataset.uploaded_chunks = ','.join(list(uploaded_chunks))
            dataset.save()
            api_logger.debug(f'当前分块长度:{len(dataset.uploaded_chunks.split(","))}, 获取分块长度:{total_chunks}')
            if len(dataset.uploaded_chunks.split(',')) == int(total_chunks):
                api_logger.debug(f'文件全部接收, 开始合并:{save_directory}/*.part*')
                uploaded = True
                with open(dataset.file_full_path, 'wb') as uploaded_file:
                    for index in range(int(total_chunks)):
                        chunk_file = os.path.join(save_directory, f'{file_name}.part{index+1}')
                        api_logger.debug(f'当前文件{chunk_file}')
                        try:
                            chunk_file = open(chunk_file, 'rb')  # 按序打开每个分片
                            uploaded_file.write(chunk_file.read())  # 读取分片内容写入新文件
                            chunk_file.close()
                        except Exception as error:
                            api_logger.error(f'合并文件:{file_name} form {save_directory}失败:{error}')
                            uploaded = False
                            # 检查合并后的MD5
                uploaded_file_md5 = check_md5_sum(file_name=dataset.file_full_path)
                if uploaded_file_md5 != file_md5:
                    api_logger.debug(f'合并文件MD5不一致:{uploaded_file_md5}, {file_md5}')
                    uploaded = False
                if uploaded:
                    dataset.uploaded = uploaded
                    dataset.save()
                    shutil.rmtree(save_directory)
                    result = {'success': True, 'messages': '成功上传文件并合并!',
                              'results': {'uploaded': uploaded, 'total_chunks': total_chunks,
                                          'file_name': file_name, 'file_md5': file_md5}}
                    return Response(result, status=status.HTTP_200_OK)
                else:
                    result = {'success': False, 'messages': '合并文件失败, 请重新上传!'}
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                result = {'success': True, 'messages': f'成功上传分块文件:{chunk_index}!',
                          'results': {'uploaded': False, 'total_chunks': total_chunks,
                                      'file_name': file_name, 'file_md5': file_md5}
                          }
                return Response(result, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return DataSetActionSerializer
        if self.action == 'retrieve':
            return DataSetDetailSerializer
        return DataSetListSerializer
