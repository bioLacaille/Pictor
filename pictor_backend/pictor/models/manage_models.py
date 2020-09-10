"""
Author: Alan Fu
Email: fualan1990@gmail.com
系统管理数据模块
"""
from django.db import models
from django.utils import timezone
from pictor.configures import NOTIFY_INFO, NOTIFY_URGENT, NOTIFY_VERY_URGENT, NOTIFY_WARNING, NOTIFY_ERROR, NOTIFY_LEVEL


class AnalysisTaskInterfaceManager(models.Manager):

    def get_active(self):
        return self.filter(is_active=True)


class AnalysisTaskInterface(models.Model):
    name = models.CharField(max_length=255, verbose_name='接口名称')
    domain = models.CharField(max_length=255, verbose_name='接口域名')
    success_code = models.CharField(max_length=255, verbose_name='成功返回码')
    error_code = models.CharField(max_length=255, verbose_name='失败返回码')
    start_uri = models.CharField(max_length=255, verbose_name='启动任务URI')
    stop_uri = models.CharField(max_length=255, verbose_name='停止任务URI')
    continue_uri = models.CharField(max_length=255, verbose_name='继续运行任务URI')
    reset_uri = models.CharField(max_length=255, verbose_name='重置任务URI')
    status_uri = models.CharField(max_length=255, verbose_name='查询任务状态URI')
    result_uri = models.CharField(max_length=255, verbose_name='获取任务结果URI')
    log_uri = models.CharField(max_length=255, verbose_name='获取运行日志URI')
    is_active = models.BooleanField(default=False, verbose_name='是否启用该配置')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        verbose_name = '分析任务接口'
        verbose_name_plural = '分析任务接口'

    def save(self, *args, **kwargs):
        super(AnalysisTaskInterface, self).save(*args, **kwargs)
        if self.is_active:
            AnalysisTaskInterface.objects.exclude(id=self.id).update(is_active=False)

    def __str__(self):
        return self.name

    objects = AnalysisTaskInterfaceManager()


class AnalysisModuleTaskInterfaceManager(models.Manager):

    def get_active(self):
        return self.filter(is_active=True)


class AnalysisModuleTaskInterface(models.Model):
    name = models.CharField(max_length=255, verbose_name='接口名称')
    domain = models.CharField(max_length=255, verbose_name='接口域名')
    success_code = models.CharField(max_length=255, verbose_name='成功返回码')
    error_code = models.CharField(max_length=255, verbose_name='失败返回码')
    install_uri = models.CharField(max_length=255, verbose_name='安装模块URI')
    status_uri = models.CharField(max_length=255, verbose_name='查询状态URI')
    reinstall_uri = models.CharField(max_length=255, verbose_name='重新安装模块URI')
    is_active = models.BooleanField(default=False, verbose_name='是否启用该配置')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        verbose_name = '分析模块接口'
        verbose_name_plural = '分析模块接口'

    def save(self, *args, **kwargs):
        super(AnalysisModuleTaskInterface, self).save(*args, **kwargs)
        if self.is_active:
            AnalysisModuleTaskInterface.objects.exclude(id=self.id).update(is_active=False)

    def __str__(self):
        return self.name

    objects = AnalysisModuleTaskInterfaceManager()


class NotificationRuleManager(models.Manager):

    def get_level_desc(self, level_key=NOTIFY_INFO):
        notification_rule = self.filter(is_active=True).first()
        if notification_rule:
            if level_key == NOTIFY_INFO:
                return notification_rule.info_level
            if level_key == NOTIFY_URGENT:
                return notification_rule.urgent_level
            if level_key == NOTIFY_VERY_URGENT:
                return notification_rule.very_urgent_level
            if level_key == NOTIFY_WARNING:
                return notification_rule.waning_level
            if level_key == NOTIFY_ERROR:
                return notification_rule.error_level
        else:
            return NOTIFY_LEVEL[level_key]

    def get_active(self):
        return self.filter(is_active=True)


class NotificationRule(models.Model):
    """通知规则"""
    name = models.CharField(max_length=255, verbose_name='规则名称')
    is_email = models.BooleanField(default=False, verbose_name='是否发送邮件')
    is_notify = models.BooleanField(default=True, verbose_name='是否发送站内信')
    email_user_ssl = models.BooleanField(default=True, verbose_name='是否使用SSL')
    email_host = models.CharField(max_length=255, blank=True, null=True, verbose_name='发送邮箱服务器',
                                  help_text='smtp.exmail.qq.com')
    email_port = models.CharField(max_length=255, null=True, blank=True, verbose_name='发送邮箱端口', help_text='465')
    email_host_user = models.CharField(max_length=255, null=True, blank=True, verbose_name='发送邮箱帐号')
    email_host_password = models.CharField(max_length=255, null=True, blank=True, verbose_name='发送邮箱密码')
    email_from_title = models.CharField(max_length=255, null=True, blank=True, verbose_name='发件人名称',
                                        help_text='Pictor <support@pictor.com.cn>')
    info_level = models.CharField(max_length=255, null=True, blank=True, verbose_name='通知等级', default='通知')
    urgent_level = models.CharField(max_length=255, null=True, blank=True, verbose_name='紧急等级', default='紧急')
    very_urgent_level = models.CharField(max_length=255, null=True, blank=True, verbose_name='非常紧急等级', default='非常紧急')
    warning_level = models.CharField(max_length=255, null=True, blank=True, verbose_name='警告等级', default='警告')
    error_level = models.CharField(max_length=255, null=True, blank=True, verbose_name='错误等级', default='错误')
    is_active = models.BooleanField(default=False, verbose_name='是否启用该配置')
    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "系统消息规则管理"
        verbose_name_plural = "系统消息规则管理"

    def save(self, *args, **kwargs):
        super(NotificationRule, self).save(*args, **kwargs)
        if self.is_active:
            NotificationRule.objects.exclude(id=self.id).update(is_active=False)

    objects = NotificationRuleManager()


class AnnouncementManager(models.Manager):

    def get_publish(self):
        return self.filter(is_active=True)


class Announcement(models.Model):
    title = models.CharField(max_length=255, verbose_name='公告标题')
    content = models.TextField(null=True, blank=True, verbose_name='公告内容')
    link = models.URLField(null=True, blank=True, verbose_name='跳转链接')
    is_publish = models.BooleanField(default=False, verbose_name='是否发布')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        db_table = 'announcement'
        verbose_name = '公告管理'
        verbose_name_plural = '公告管理'

    def __str__(self):
        return self.title

    objects = AnnouncementManager()


class WorkZoneSerialNumberRuleManager(models.Manager):

    def get_active(self):
        return self.filter(is_active=True)


class WorkZoneSerialNumberRule(models.Model):
    # todo: 暂定不需要, 确认后处理
    name = models.CharField(max_length=255, verbose_name='规则名称')
    start_string = models.CharField(max_length=255, verbose_name='前缀字符', help_text='开头使用的字符', default='workZone')
    middle_string_len = models.IntegerField(default=6, verbose_name='中间字符生成长度', help_text='中间字符生成长度')
    end_string = models.CharField(max_length=255, null=True, blank=True, verbose_name='后缀字符', help_text='默认为无', default='')
    spilt_string = models.CharField(max_length=255, verbose_name='分割字符', help_text='默认为-', default='-')
    is_active = models.BooleanField(default=False, verbose_name='是否启用该配置')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')

    class Meta:
        db_table = 'work_zone_setting'
        verbose_name = '工作区编号规则'
        verbose_name_plural = '工作区编号规则'

    def save(self, *args, **kwargs):
        super(WorkZoneSerialNumberRule, self).save(*args, **kwargs)
        if self.is_active:
            WorkZoneSerialNumberRule.objects.exclude(id=self.id).update(is_active=False)

    def __str__(self):
        return self.name

    objects = WorkZoneSerialNumberRuleManager()