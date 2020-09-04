from rest_framework import serializers
from pictor.models import AnalysisSerialNumberSetting, ProjectSerialNumberSetting, SampleSerialNumberSetting, \
    SequencingSerialNumberSetting
from pictor.serializers.workzone_serializers import WorkZoneBaseSerializer


class AnalysisSerialNumberSettingSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='创建时间')

    class Meta:
        model = AnalysisSerialNumberSetting
        fields = '__all__'


class ProjectSerialNumberSettingSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='创建时间')

    class Meta:
        model = ProjectSerialNumberSetting
        fields = '__all__'


class SampleSerialNumberSettingSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='创建时间')

    class Meta:
        model = SampleSerialNumberSetting
        fields = '__all__'


class SequencingSerialNumberSettingSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='创建时间')

    class Meta:
        model = SequencingSerialNumberSetting
        fields = '__all__'
