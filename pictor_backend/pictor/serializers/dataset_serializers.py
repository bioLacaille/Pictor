from rest_framework import serializers
from pathlib import Path
from pictor.models import DataSet
from pictor.serializers.user_serializers import UserBaseSerializer
from pictor.serializers.project_serializers import ProjectBaseSerializer
from pictor.configures import DATASET_TYPE, FILE_TYPE


class DataSetListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    edit_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")
    file_uri = serializers.SerializerMethodField(read_only=True)
    relative_path = serializers.SerializerMethodField(read_only=True)
    suffix = serializers.SerializerMethodField(read_only=True)

    def get_file_uri(self, obj):
        return obj.file_uri

    def get_relative_path(self, obj):
        return obj.relative_path

    def get_suffix(self, obj):
        return Path(obj.file_name).suffix.replace(".", "")

    class Meta:
        model = DataSet
        fields = '__all__'


class DataSetActionSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    edit_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.creator = self.context['request'].user
        instance.save()
        return instance

    class Meta:
        model = DataSet
        fields = '__all__'


class DataSetDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    edit_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")
    file_uri = serializers.SerializerMethodField(read_only=True)
    suffix = serializers.SerializerMethodField(read_only=True)
    relative_path = serializers.SerializerMethodField(read_only=True)

    def get_file_uri(self, obj):
        return obj.file_uri

    def get_relative_path(self, obj):
        return obj.relative_path

    def get_suffix(self, obj):
        return Path(obj.file_name).suffix.replace(".", "")

    class Meta:
        model = DataSet
        fields = '__all__'

