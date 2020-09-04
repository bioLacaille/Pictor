from rest_framework import serializers
from pictor.models import NotificationRule, AnalysisTaskInterface, SequencingTaskInterface, AnalysisModuleTaskInterface, \
    Announcement
from pictor.configures import NOTIFY_LEVEL, NOTIFY_INFO, NOTIFY_URGENT, NOTIFY_VERY_URGENT, NOTIFY_WARNING, NOTIFY_ERROR


class NotificationRuleSerializer(serializers.ModelSerializer):
    """消息规则"""
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='创建时间')

    class Meta:
        model = NotificationRule
        fields = '__all__'


class NotificationRuleDetailSerializer(serializers.ModelSerializer):
    """消息规则"""
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='创建时间')
    info_level = serializers.SerializerMethodField(read_only=True, label='通知等级')
    urgent_level = serializers.SerializerMethodField(read_only=True, label='紧急等级')
    very_urgent_level = serializers.SerializerMethodField(read_only=True, label='非常紧急等级')
    warning_level = serializers.SerializerMethodField(read_only=True, label='警告等级')
    error_level = serializers.SerializerMethodField(read_only=True, label='错误等级')

    def get_info_level(self, obj):
        if obj.info_level:
            return obj.info_level
        else:
            return NOTIFY_LEVEL.get(NOTIFY_INFO, NOTIFY_INFO)

    def get_urgent_level(self, obj):
        if obj.urgent_level:
            return obj.urgent_level
        else:
            return NOTIFY_LEVEL.get(NOTIFY_URGENT, NOTIFY_URGENT)

    def get_very_urgent_level(self, obj):
        if obj.very_urgent_level:
            return obj.very_urgent_level
        else:
            return NOTIFY_LEVEL.get(NOTIFY_VERY_URGENT, NOTIFY_VERY_URGENT)

    def get_warning_level(self, obj):
        if obj.warning_level:
            return obj.warning_level
        else:
            return NOTIFY_LEVEL.get(NOTIFY_WARNING, NOTIFY_WARNING)

    def get_error_level(self, obj):
        if obj.error_level:
            return obj.error_level
        else:
            return NOTIFY_LEVEL.get(NOTIFY_ERROR, NOTIFY_ERROR)

    class Meta:
        model = NotificationRule
        fields = '__all__'


########################################################################################


class AnalysisTaskInterfaceSerializer(serializers.ModelSerializer):
    """分析任务接口"""
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='创建时间')

    class Meta:
        model = AnalysisTaskInterface
        fields = '__all__'


class AnalysisModuleTaskInterfaceSerializer(serializers.ModelSerializer):
    """分析模块接口"""
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='创建时间')

    class Meta:
        model = AnalysisModuleTaskInterface
        fields = '__all__'


class SequencingTaskInterfaceSerializer(serializers.ModelSerializer):
    """拆分任务接口"""
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='创建时间')

    class Meta:
        model = SequencingTaskInterface
        fields = '__all__'


class AnnouncementSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='创建时间')

    class Meta:
        model = Announcement
        fields = '__all__'