"""
Author: Alan Fu
Email: fualan1990@gmail.com
系统设置数据模块
"""
from django.db import models
from django.utils import timezone


class ProjectSerialNumberSettingManager(models.Manager):

    def get_active(self, work_zone=None):
        if work_zone:
            return self.filter(is_active=True, work_zone=work_zone)
        else:
            return self.filter(is_active=True)


class ProjectSerialNumberSetting(models.Model):
    work_zone = models.ForeignKey('WorkZone', verbose_name='所属工作区', null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name='project_number_settings')
    name = models.CharField(max_length=255, verbose_name='规则名称')
    start_string = models.CharField(max_length=255, verbose_name='前缀字符', help_text='开头使用的字符', default='analysis')
    middle_string_len = models.IntegerField(default=6, verbose_name='中间字符生成长度', help_text='中间字符生成长度')
    end_string = models.CharField(max_length=255, null=True, blank=True, verbose_name='后缀字符', help_text='默认为无', default='')
    spilt_string = models.CharField(max_length=255, verbose_name='分割字符', help_text='默认为-', default='-')
    is_active = models.BooleanField(default=False, verbose_name='是否启用该配置')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        db_table = 'project_number_setting'
        verbose_name = '项目编号规则'
        verbose_name_plural = '项目编号规则'

    def save(self, *args, **kwargs):
        super(ProjectSerialNumberSetting, self).save(*args, **kwargs)
        if self.is_active:
            ProjectSerialNumberSetting.objects.exclude(id=self.id).update(is_active=False)

    def __str__(self):
        return self.name

    objects = ProjectSerialNumberSettingManager()


class SampleSerialNumberSettingManager(models.Manager):

    def get_active(self, work_zone=None):
        if work_zone:
            return self.filter(is_active=True, work_zone=work_zone)
        else:
            return self.filter(is_active=True)


class SampleSerialNumberSetting(models.Model):
    work_zone = models.ForeignKey('WorkZone', verbose_name='所属工作区', null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name='sample_number_settings')
    name = models.CharField(max_length=255, verbose_name='规则名称')
    start_string = models.CharField(max_length=255, verbose_name='前缀字符', help_text='开头使用的字符', default='sample')
    middle_string_len = models.IntegerField(default=6, verbose_name='中间字符生成长度', help_text='中间字符生成长度')
    end_string = models.CharField(max_length=255, null=True, blank=True, verbose_name='后缀字符', help_text='默认为无', default='')
    spilt_string = models.CharField(max_length=255, verbose_name='分割字符', help_text='默认为-', default='-')
    is_active = models.BooleanField(default=False, verbose_name='是否启用该配置')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        db_table = 'sample_number_setting'
        verbose_name = '样本编号规则'
        verbose_name_plural = '样本编号规则'

    def save(self, *args, **kwargs):
        super(SampleSerialNumberSetting, self).save(*args, **kwargs)
        if self.is_active:
            SampleSerialNumberSetting.objects.exclude(id=self.id).update(is_active=False)

    def __str__(self):
        return self.name

    objects = SampleSerialNumberSettingManager()


class AnalysisSerialNumberSettingManager(models.Manager):

    def get_active(self, work_zone=None):
        if work_zone:
            return self.filter(is_active=True, work_zone=work_zone)
        else:
            return self.filter(is_active=True)


class AnalysisSerialNumberSetting(models.Model):
    work_zone = models.ForeignKey('WorkZone', verbose_name='所属工作区', null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name='analysis_number_settings')
    name = models.CharField(max_length=255, verbose_name='规则名称')
    start_string = models.CharField(max_length=255, verbose_name='前缀字符', help_text='开头使用的字符', default='analysis')
    middle_string_len = models.IntegerField(default=6, verbose_name='中间字符生成长度', help_text='中间字符生成长度')
    end_string = models.CharField(max_length=255, null=True, blank=True, verbose_name='后缀字符', help_text='默认为无', default='')
    spilt_string = models.CharField(max_length=255, verbose_name='分割字符', help_text='默认为-', default='-')
    is_active = models.BooleanField(default=False, verbose_name='是否启用该配置')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        db_table = 'analysis_number_setting'
        verbose_name = '分析编号规则配置'
        verbose_name_plural = '分析编号规则配置'

    def save(self, *args, **kwargs):
        super(AnalysisSerialNumberSetting, self).save(*args, **kwargs)
        if self.is_active:
            AnalysisSerialNumberSetting.objects.exclude(id=self.id).update(is_active=False)

    def __str__(self):
        return self.name

    objects = AnalysisSerialNumberSettingManager()


class FileUploadSettingManager(models.Manager):

    def get_active(self):
        return self.filter(is_active=True)


class FileUploadSetting(models.Model):
    # todo: 暂定不需要, 确认后处理
    work_zone = models.ForeignKey('WorkZone', verbose_name='所属工作区', null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name='upload_settings')
    name = models.CharField(max_length=255,  verbose_name='规则名称')
    accept_files = models.CharField(max_length=255, default='*', verbose_name='文件类型')
    max_size = models.IntegerField(default=1073741824, verbose_name='最大限制')
    allow_upload_directory = models.BooleanField(default=True, verbose_name='是否允许上传文件夹')
    auto_upload = models.BooleanField(default=True, verbose_name='是否自动开始上传')

    class Meta:
        verbose_name = '上传规则配置'
        verbose_name_plural = '上传规则配置'

    def __str__(self):
        return self.name

    objects = FileUploadSettingManager()
