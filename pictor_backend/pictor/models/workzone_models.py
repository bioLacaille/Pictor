"""
Author: Alan Fu
Email: fualan1990@gmail.com
工作区数据模块
"""
from django.db import models
from django.utils import timezone
from pictor.configures import MEMBER_TYPE, ZONE_GUEST
from pictor.utils.base_heplers import change_dict_for_model_choices


class WorkZone(models.Model):
    serial_number = models.CharField(max_length=255, verbose_name='工作区编号')
    name = models.CharField(max_length=255, verbose_name='工作区名称')
    remark = models.TextField(null=True, blank=True, verbose_name='备注/描述')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
    creator = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者',
                                related_name='work_zones')

    class Meta:
        db_table = 'work_zone'
        verbose_name = '工作区'
        verbose_name_plural = '工作区'

    def __str__(self):
        return self.serial_number


class WorkZoneMember(models.Model):
    work_zone = models.ForeignKey('WorkZone', verbose_name='所属工作区', on_delete=models.CASCADE,
                                  related_name='work_zone_members')
    user = models.ForeignKey('User', verbose_name='所属用户', on_delete=models.CASCADE, related_name='work_zone_members')
    level = models.IntegerField(default=ZONE_GUEST, choices=change_dict_for_model_choices(MEMBER_TYPE),
                                verbose_name='成员级别')
    remark = models.TextField(null=True, blank=True, verbose_name='备注/描述')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
    creator = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者',
                                related_name='creator_work_zone_members')

    class Meta:
        db_table = 'work_zone_member'
        verbose_name = '工作区成员'
        verbose_name_plural = '工作区成员'

    def __str__(self):
        return f'{self.work_zone.__str__()}@{self.user.__str__()}'
