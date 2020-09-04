from rest_framework import serializers
from pictor.models import Project
from pictor.serializers.user_serializers import UserBaseSerializer
from pictor.serializers.workzone_serializers import WorkZoneBaseSerializer


class ProjectBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'serial_number', 'name')


class ProjectActionSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.creator = self.context['request'].user
        instance.save()
        return instance

    class Meta:
        model = Project
        fields = '__all__'


class ProjectDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")
    work_zone = WorkZoneBaseSerializer(read_only=True, label="所属工作区")

    class Meta:
        model = Project
        fields = '__all__'

