"""
Author: Alan Fu
Email: fualan1990@gmail.com
拆分数据模块
"""
from django.db import models
from django.utils import timezone
from pictor.utils.base_heplers import change_dict_for_model_choices, change_list_for_model_choices


# 上传文件目录
def upload_path(instance, filename):
    file_path = 'sample_sheet/{serial_number}/{filename}'.format(
        serial_number=instance.serial_number,
        filename=filename
    )
    return file_path

#
# class Sequencing(models.Model):
#     work_zone = models.ForeignKey('WorkZone', verbose_name='所属工作区', null=True, blank=True, on_delete=models.SET_NULL,
#                                   related_name='sequencing')
#     serial_number = models.CharField(max_length=255, verbose_name='任务编号')
#     sample_sheet = models.FileField(verbose_name='sample_sheet信息', upload_to=upload_path)
#     batch_number = models.CharField(max_length=255, verbose_name='批次编号')
#     start_strategy = models.CharField(max_length=255, choices=change_list_for_model_choices(START_STRATEGY),
#                                       null=True, blank=True, verbose_name='上机策略')
#     split_strategy = models.CharField(max_length=255, choices=change_list_for_model_choices(SPLIT_STRATEGY),
#                                       null=True, blank=True, verbose_name='拆分策略')
#     sequencing_strategy = models.CharField(max_length=255, choices=change_list_for_model_choices(SEQUENCING_STRATEGY),
#                                            null=True, blank=True, verbose_name='测序策略')
#     index_mismatch = models.CharField(max_length=255, choices=change_dict_for_model_choices(INDEX_MISMATCH),
#                                       null=True, blank=True, verbose_name='index错配数')
#     read_length = models.CharField(max_length=255, null=True, blank=True, verbose_name='测序读长')
#     sequencing_kit = models.CharField(max_length=255, null=True, blank=True, verbose_name='测序试剂盒')
#     auto_connector = models.BooleanField(default=False, null=True, blank=True, verbose_name='是否自动去接头')
#     status = models.IntegerField(default=SEQ_UN_START, choices=change_dict_for_model_choices(SEQUENCING_STATUS),
#                                  null=True, blank=True, verbose_name='状态')
#     process = models.CharField(max_length=255, null=True, blank=True, verbose_name='进度')
#     started_time = models.DateTimeField(null=True, blank=True, verbose_name='启动时间')
#     finished_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
#     remark = models.TextField(null=True, blank=True, verbose_name='备注/描述')
#     created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
#     creator = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者',
#                                 related_name='sequencing')
#
#     class Meta:
#         verbose_name = '拆分任务'
#         verbose_name_plural = '拆分任务'
#
#     def __str__(self):
#         return self.serial_number
#
#
# class SequencingResult(models.Model):
#     sequencing = models.ForeignKey('Sequencing', on_delete=models.CASCADE, verbose_name='所属测序任务',
#                                    related_name='sequencing_results')
#     output_data_num = models.FloatField(default=0, null=True, blank=True, verbose_name='产出数据量')
#     output_reads_num = models.FloatField(default=0, null=True, blank=True, verbose_name='产出Reads数')
#     output_q20_ratio = models.FloatField(default=0, null=True, blank=True, verbose_name='Q20占比')
#     output_q30_ratio = models.FloatField(default=0, null=True, blank=True, verbose_name='Q30占比')
#     avg_quality_num = models.FloatField(default=0, null=True, blank=True, verbose_name='平均质量值')
#     remark = models.TextField(null=True, blank=True, verbose_name='备注')
#     created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
#     is_deleted = models.BooleanField(default=False, verbose_name='是否已经删除')
#     creator = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='创建者',
#                                 related_name='sequencing_results')
#
#     class Meta:
#         verbose_name = '拆分任务统计结果'
#         verbose_name_plural = '拆分任务统计结果'
#
#     def __str__(self):
#         return self.sequencing.serial_number
