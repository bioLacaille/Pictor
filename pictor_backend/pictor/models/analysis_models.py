"""
Author: Alan Fu
Email: fualan1990@gmail.com
分析数据模块
"""
from django.db import models
from django.utils import timezone
import os
from django.conf import settings
from pictor.configures import ANALYSIS_MODULE_STATUS, ANALYSIS_STATUS, ANALYSIS_MODULE_TYPE, GIT, LOCAL
from pictor.utils.base_heplers import change_dict_for_model_choices, create_or_get_directory


# 上传文件目录
def upload_module_path(instance, filename):
    file_path = 'AnalysisModule/{module_name}/{version}/{filename}'.format(
        module_name=instance.name,
        version=instance.version,
        filename=filename
    )
    return file_path


class AnalysisModule(models.Model):
    module_type = models.IntegerField(choices=change_dict_for_model_choices(ANALYSIS_MODULE_TYPE), verbose_name='模块类型')
    name = models.CharField(max_length=255, verbose_name='模块名称')
    command = models.CharField(max_length=255, verbose_name='运行命令')
    url = models.CharField(null=True, blank=True, max_length=255, verbose_name='git链接路径')
    pipeline_file = models.FileField(null=True, blank=True, upload_to=upload_module_path, verbose_name='模块主流程文件')
    version = models.CharField(max_length=255, null=True, blank=True, verbose_name='版本号/分支名')
    developer = models.CharField(max_length=255, null=True, blank=True, verbose_name='开发者')
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name='开发者邮箱')
    status = models.IntegerField(default=10, choices=change_dict_for_model_choices(ANALYSIS_MODULE_STATUS),
                                 null=True, blank=True, verbose_name='状态')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
    creator = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者',
                                related_name='analysis_modules')

    class Meta:
        verbose_name = '分析模块'
        verbose_name_plural = '分析模块'

    def __str__(self):
        return self.name

    @property
    def file_path(self):
        data_path = ''
        if self.module_type == GIT:
            version_split = self.version.split('/')
            version_type = version_split[1]
            version = version_split[2]
            base_path = create_or_get_directory(os.path.join(settings.MEDIA_ROOT, 'AnalysisModule'))
            data_path = create_or_get_directory(os.path.join(base_path, self.name, version_type, version))
        if self.module_type == LOCAL:
            data_path = os.path.dirname(self.pipeline_file.path)
        return data_path

    @property
    def file_uri(self):
        data_path = ''
        if self.module_type == GIT:
            version_split = self.version.split('/')
            version_type = version_split[1]
            version = version_split[2]
            base_path = os.path.join(settings.MEDIA_URL, 'AnalysisModule')
            data_path = os.path.join(base_path, self.name, version_type, version)
        if self.module_type == LOCAL:
            data_path = os.path.dirname(self.pipeline_file.url)
        return data_path


class AnalysisParameter(models.Model):
    module = models.ForeignKey(AnalysisModule, on_delete=models.CASCADE, verbose_name='所属分析模块',
                               related_name='module_parameters')
    name = models.CharField(max_length=255, verbose_name='参数名称')
    detail = models.TextField(verbose_name='参数详情')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
    creator = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者',
                                related_name='analysis_parameters')

    class Meta:
        verbose_name = '分析参数'
        verbose_name_plural = '分析参数'

    def __str__(self):
        return self.name


class Analysis(models.Model):
    work_zone = models.ForeignKey('WorkZone', verbose_name='所属工作区', null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name='analyses')
    project = models.ForeignKey('Project', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属项目',
                                related_name='analyses')
    analysis_module = models.ForeignKey('AnalysisModule', null=True, blank=True, related_name='analyses',
                                        verbose_name='所属分析任务', on_delete=models.SET_NULL)
    serial_number = models.CharField(max_length=255, verbose_name='任务编号')
    command = models.CharField(max_length=255, verbose_name='运行命令')
    analysis_parameter = models.TextField(blank=True, verbose_name='分析参数详情')
    is_email = models.BooleanField(default=False, verbose_name='是否发送邮件')
    email_list = models.TextField(default='', null=True, blank=True, verbose_name='通知邮箱地址', help_text='逗号分割多个邮箱')
    status = models.IntegerField(default=10, choices=change_dict_for_model_choices(ANALYSIS_STATUS),
                                 null=True, blank=True, verbose_name='状态')
    process = models.CharField(max_length=255, null=True, blank=True, verbose_name='进度')
    started_time = models.DateTimeField(null=True, blank=True, verbose_name='启动时间')
    finished_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
    creator = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者',
                                related_name='analyses')

    class Meta:
        verbose_name = '分析任务'
        verbose_name_plural = '分析任务'

    def __str__(self):
        return self.serial_number