"""
Author: Alan Fu
Email: fualan1990@gmail.com
站内消息数据模型
"""
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.db.models import QuerySet
from django.utils.html import escape
from django.utils.timesince import timesince
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.utils import timezone
from pictor.configures import NOTIFY_LEVEL, NOTIFY_INFO
from pictor.utils.base_heplers import change_dict_for_model_choices


class NotificationQueryset(QuerySet):
    def get_read(self):
        """
        返回未标记删除且已读的小时
        """
        return self.filter(is_deleted=False, is_read=True)

    def get_unread(self):
        """
        返回未标记删除且未读的小时
        """
        return self.filter(is_deleted=False, is_read=False)

    def get_important(self):
        """
        返回重要邮件
        """
        return self.filter(is_deleted=False, is_important=True)

    def get_unimportant(self):
        """
        返回非重要邮件
        """
        return self.filter(is_deleted=False, is_important=False)

    def get_deleted(self):
        """
        :return: Soft deleted notification filter()
        """
        return self.filter(is_deleted=True)

    def get_active(self):
        """
        返回未标记删除的通知
        """
        return self.filter(is_deleted=False)

    def active(self):
        """
        恢复通知，标记为未删除
        """
        self.update(is_deleted=False)

    def deleted(self):
        """
        删除通知
        """
        self.update(is_deleted=True)

    def read(self):
        """
        标记为已读
        """
        self.update(is_read=True)

    def unread(self):
        """
        标记为未读
        """
        self.update(is_read=False)

    def important(self):
        """
        标记为重要
        """
        self.update(is_important=True)

    def unimportant(self):
        """
        标记为重要
        """
        self.update(is_important=False)

    def unread_all(self, user=None):
        """
        标记所有已读为未读
        """
        qs = self.get_read()
        if user:
            qs = qs.filter(recipient=user)
        qs.update(is_read=False)

    def read_all(self, user=None):
        """
        标记所有未读为已读
        """
        qs = self.get_unread()
        if user:
            qs = qs.filter(recipient=user)
        qs.update(is_read=True)

    def delete_all(self, user=None):
        """
        删除标记所有未读和已读消息
        """
        qs = self.get_active()
        if user:
            qs = qs.filter(recipient=user)
        qs.update(is_deleted=True)

    def active_all(self, user=None):
        """
        恢复所有已删除消息
        """
        qs = self.get_deleted()
        if user:
            qs = qs.filter(recipient=user)
        qs.update(is_deleted=False)

    def important_all(self, user=None):
        qs = self.get_active()
        if user:
            qs = qs.filter(recipient=user)
        qs.update(is_important=True)

    def unimportant_all(self, user=None):
        qs = self.get_active()
        if user:
            qs = qs.filter(recipient=user)
        qs.update(is_important=False)


class Notification(models.Model):
    object_type = models.ForeignKey(
        ContentType, null=True, blank=True,
        related_name='type_notifications', on_delete=models.CASCADE,
        verbose_name="对象类型")
    object_id = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="对象ID")
    content_object = GenericForeignKey('object_type', 'object_id')
    level = models.PositiveIntegerField(choices=change_dict_for_model_choices(NOTIFY_LEVEL), default=NOTIFY_INFO,
                                        verbose_name="消息级别")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recipient_notifications',
                                  on_delete=models.CASCADE, verbose_name="接收者")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='sender_notifications',
                               on_delete=models.CASCADE, verbose_name="发送者", help_text='当消息为系统发出时为空')
    title = models.CharField(max_length=255, verbose_name="消息标题")
    content = models.TextField(blank=True, verbose_name="具体消息内容")
    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    is_deleted = models.BooleanField(default=False, verbose_name="是否已删除")
    is_important = models.BooleanField(default=False, verbose_name="是否重要邮件")

    objects = NotificationQueryset.as_manager()

    class Meta(object):
        verbose_name = "通知消息"
        verbose_name_plural = "通知消息"

    def __str__(self):
        return f'{self.title} at {timesince(self.created_time)}'

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        self.is_read = False
        self.save()

    def mark_as_deleted(self):
        self.is_deleted = True
        self.save()

    def mark_as_active(self):
        self.is_deleted = False
        self.save()

    def mark_as_important(self):
        self.is_important = True
        self.save()

    def mark_as_unimportant(self):
        self.is_important = False
        self.save()

    @cached_property
    def object(self):
        return self.content_object

    @staticmethod
    def do_escape(obj):
        return escape(force_text(obj)) if obj else None
