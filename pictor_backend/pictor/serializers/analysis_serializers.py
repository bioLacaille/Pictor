from rest_framework import serializers
import json
from pictor.models import AnalysisModule, Analysis, AnalysisParameter
from pictor.serializers.user_serializers import UserBaseSerializer
from pictor.serializers.project_serializers import ProjectBaseSerializer
from pictor.configures import ANALYSIS_MODULE_TYPE, ANALYSIS_MODULE_STATUS, ANALYSIS_STATUS


class AnalysisModuleBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnalysisModule
        fields = ('id', 'name', 'version', 'command', 'module_type', 'remark', 'file_uri')


class AnalysisModuleActionSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.creator = self.context['request'].user
        instance.save()
        return instance

    class Meta:
        model = AnalysisModule
        fields = '__all__'


class AnalysisModuleListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")

    class Meta:
        model = AnalysisModule
        fields = '__all__'


class AnalysisModuleDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")
    status = serializers.SerializerMethodField(read_only=True)
    pipeline_file = serializers.SerializerMethodField(read_only=True)
    file_uri = serializers.SerializerMethodField(read_only=True)

    def get_status(self, obj):
        return ANALYSIS_MODULE_STATUS.get(obj.status, obj.status)

    def get_file_uri(self, obj):
        return obj.file_uri

    def get_pipeline_file(self, obj):
        if obj.pipeline_file:
            return {"name": obj.pipeline_file.name, "url": obj.pipeline_file.url}
        else:
            return None

    class Meta:
        model = AnalysisModule
        fields = '__all__'

#########################################################################################


class AnalysisParameterBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnalysisParameter
        fields = ('id', 'name', 'detail')


class AnalysisParameterActionSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.creator = self.context['request'].user
        instance.save()
        return instance

    class Meta:
        model = AnalysisParameter
        fields = '__all__'


class AnalysisParameterListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")

    class Meta:
        model = AnalysisParameter
        fields = '__all__'


class AnalysisParameterDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")
    detail = serializers.SerializerMethodField(read_only=True)

    def get_detail(self, obj):
        return json.loads(obj.detail)

    class Meta:
        model = AnalysisParameter
        fields = '__all__'

#########################################################################################


class AnalysisBaseSerializer(serializers.ModelSerializer):
    analysis_module = AnalysisModuleBaseSerializer(read_only=True)
    project = ProjectBaseSerializer(read_only=True)

    class Meta:
        model = Analysis
        fields = ('id', 'serial_number', 'analysis_module', 'project')


class AnalysisActionSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.creator = self.context['request'].user
        instance.save()
        return instance

    class Meta:
        model = Analysis
        fields = '__all__'


class AnalysisListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    started_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    finished_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")
    analysis_module = AnalysisModuleBaseSerializer(read_only=True)
    project = ProjectBaseSerializer(read_only=True)

    class Meta:
        model = Analysis
        fields = '__all__'


class AnalysisDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    started_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    finished_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")
    analysis_module = AnalysisModuleBaseSerializer(read_only=True)
    project = ProjectBaseSerializer(read_only=True)
    analysis_parameter = serializers.SerializerMethodField(read_only=True)

    def get_analysis_parameter(self, obj):
        try:
            return json.loads(obj.analysis_parameter)
        except:
            return obj.analysis_parameter

    class Meta:
        model = Analysis
        fields = '__all__'