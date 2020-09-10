"""
Author: Alan Fu
Email: fualan1990@gmail.com
操作日志数据模型
"""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
import json
from pictor.configures import ACTION_TYPE
from pictor.utils.base_heplers import change_dict_for_model_choices


class LogActionManager(models.Manager):
    def create_log_action(self, **kwargs):
        """
        创建操作日志记录
        """
        request = kwargs.get('request', None)
        # 取出操作请求，从其中得到ip地址
        if request is not None:
            del kwargs['request']
            # Let's grab the current IP of the user.
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                remote_ip = x_forwarded_for.split(',')[0]
            else:
                remote_ip = request.META.get('REMOTE_ADDR')
            kwargs.setdefault('remote_ip', remote_ip)
        # 取出当前操作对象
        instance = kwargs.get('instance', None)
        if instance is not None:
            del kwargs['instance']
        # 存在操作对象，取出对象信息
        if instance is not None:
            kwargs.setdefault(
                'object_type',
                ContentType.objects.get_for_model(instance)
            )
            kwargs.setdefault('object_id', instance.id)
        action_log = self.create(**kwargs)
        return action_log

    def get_for_model(self, model):
        # 根据当前对象取出ContentType
        if not issubclass(model, models.Model):
            return self.none()
        ct = ContentType.objects.get_for_model(model)
        return self.filter(content_type=ct)


class ActionLog(models.Model):
    object_type = models.ForeignKey(
        'contenttypes.ContentType', related_name='type_action_logs', verbose_name="对象类型",
        blank=True, null=True, on_delete=models.SET_NULL
    )
    object_id = models.BigIntegerField(verbose_name="对象ID", blank=True, null=True, db_index=True)
    content_object = GenericForeignKey('object_type', 'object_id')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="所属用户",
        blank=True, null=True,
        on_delete=models.SET_NULL, related_name='user_action_logs'
    )
    action_type = models.IntegerField(verbose_name="操作类型", blank=True, null=True,
                                      choices=change_dict_for_model_choices(ACTION_TYPE))
    action_info = models.TextField(verbose_name="操作详情", blank=True, null=True)
    object_changes = models.TextField(blank=True, null=True, verbose_name="改变详情")
    remote_ip = models.GenericIPAddressField(verbose_name="请求IP地址", blank=True, null=True)
    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")

    objects = LogActionManager()

    class Meta:
        verbose_name = "操作日志"
        verbose_name_plural = "操作日志"

    def __str__(self):
        return f'{self.user}-{self.action_type}'

    def get_action_type_display(self):
        action_type = ACTION_TYPE.get(self.action_type, self.action_type)
        return action_type

    @property
    def object_changes_dict(self):
        """
        :return: The changes recorded in this log entry as a dictionary object.
        """
        try:
            return json.loads(self.object_changes)
        except ValueError:
            return {}
