"""
Author: Alan Fu
Email: fualan1990@gmail.com
项目数据模块
"""
from django.db import models
from django.utils import timezone


class Project(models.Model):
    work_zone = models.ForeignKey('WorkZone', verbose_name='所属工作区', null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='projects')
    serial_number = models.CharField(max_length=255, verbose_name='项目编号')
    name = models.CharField(max_length=255, verbose_name='项目名称')
    remark = models.TextField(null=True, blank=True, verbose_name='描述/备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
    creator = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者',
                                related_name='projects')

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def __str__(self):
        return self.serial_number
