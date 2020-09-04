"""
Author: Alan Fu
Email: fualan1990@gmail.com
样本数据模块
"""
from django.db import models
from django.utils import timezone


class Sample(models.Model):
    work_zone = models.ForeignKey('WorkZone', verbose_name='所属工作区', null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='samples')
    project = models.ForeignKey('Project', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属项目',
                                related_name='samples')
    serial_number = models.CharField(max_length=255, verbose_name='样本编号')
    sample_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='样本名称')
    sample_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='样本类型')
    sample_source = models.CharField(max_length=255, null=True, blank=True, verbose_name='样本来源')
    dataset = models.ManyToManyField('DataSet', blank=True, verbose_name='关联文件')
    remark = models.TextField(null=True, blank=True, verbose_name='描述/备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
    creator = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者',
                                related_name='samples')

    class Meta:
        verbose_name = '样本'
        verbose_name_plural = '样本'

    def __str__(self):
        return self.serial_number
