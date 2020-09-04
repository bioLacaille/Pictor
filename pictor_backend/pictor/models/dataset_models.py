"""
Author: Alan Fu
Email: fualan1990@gmail.com
文件数据模块
"""
from django.db import models
from django.utils import timezone
from pictor.utils.base_heplers import change_dict_for_model_choices
from pictor.configures import DATASET_TYPE, FILE_TYPE, PUBLIC_DATA, FILE
import uuid
import os
from pictor.utils.dataset_helpers import get_data_uri, get_data_directory_path


class DataSet(models.Model):
    work_zone = models.ForeignKey('WorkZone', verbose_name='所属工作区', null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name='dataset')
    serial_number = models.CharField(max_length=255, verbose_name='文件编号')
    directory_path = models.CharField(default='', max_length=255, verbose_name='目录路径')
    file_name = models.CharField(max_length=255, verbose_name='文件名称')
    data_type = models.IntegerField(default=PUBLIC_DATA, choices=change_dict_for_model_choices(DATASET_TYPE),
                                    verbose_name='数据类型')
    file_type = models.IntegerField(default=FILE, choices=change_dict_for_model_choices(FILE_TYPE), verbose_name='文件类型')
    file_size = models.IntegerField(default=0, verbose_name='文件大小(KB)')
    uploaded = models.BooleanField(default=False, verbose_name='是否完整上传')
    file_md5 = models.CharField(default='', max_length=255, verbose_name='文件MD5')
    uploaded_chunks = models.TextField(default='', verbose_name='已上传的分块(逗号分割)')
    total_chunks = models.IntegerField(default=0, verbose_name='文件总分片数')
    download_url = models.URLField(null=True, blank=True, verbose_name='离线上传链接')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
    edit_time = models.DateTimeField(default=timezone.now, verbose_name='修改日期')
    remark = models.TextField(null=True, blank=True, verbose_name='备注/描述')
    creator = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者',
                                related_name='dataset')

    class Meta:
        verbose_name = '文件数据'
        verbose_name_plural = '文件数据'

    def __str__(self):
        if not self.file_md5:
            return self.serial_number
        return self.file_md5

    def save(self, *args, **kwargs):
        if not self.pk:
            self.serial_number = str(uuid.uuid1())
        super(DataSet, self).save(*args, **kwargs)

    @property
    def directory_full_path(self, *args, **kwargs):
        if self.work_zone:
            work_zone_id = self.work_zone.id
        else:
            work_zone_id = None
        data_path = get_data_directory_path(data_type=self.data_type,
                                            current_path=self.directory_path,
                                            work_zone_id=work_zone_id)
        return data_path

    @property
    def file_full_path(self, *args, **kwargs):
        return os.path.join(self.directory_full_path, self.file_name)

    @property
    def file_uri(self, *args, **kwargs):
        # 若不是公共数据, 则数据保存在工作区下
        if self.work_zone_id:
            work_zone_id = self.work_zone.id
        else:
            work_zone_id = None
        data_uri = get_data_uri(data_type=self.data_type, current_path=self.directory_path,
                                work_zone_id=work_zone_id, file_name=self.file_name)
        return data_uri

    @property
    def relative_path(self):
        return os.path.join(self.directory_path, self.file_name)