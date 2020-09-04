from rest_framework import serializers
from pictor.models import Sample
from pictor.serializers.user_serializers import UserBaseSerializer
from pictor.serializers.project_serializers import ProjectBaseSerializer


class SampleListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")
    project = ProjectBaseSerializer(read_only=True, label="所属项目")
    dataset_count = serializers.SerializerMethodField(read_only=True)

    def get_dataset_count(self, obj):
        return obj.dataset.count()

    class Meta:
        model = Sample
        fields = '__all__'


class SampleActionSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.creator = self.context['request'].user
        instance.save()
        return instance

    class Meta:
        model = Sample
        fields = '__all__'


class SampleDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")
    project = ProjectBaseSerializer(read_only=True, label="所属项目")

    class Meta:
        model = Sample
        fields = '__all__'

