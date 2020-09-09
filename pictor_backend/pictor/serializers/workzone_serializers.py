"""
Author: Alan Fu
Email: fualan1990@gmail.com
工作区数据序列化
"""
from rest_framework import serializers
from pictor.models import WorkZone, WorkZoneMember
from pictor.serializers.user_serializers import UserBaseSerializer
from pictor.configures import ZONE_ADMIN
from pictor.utils.permission_heplers import get_work_zone_permission


class WorkZoneBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkZone
        fields = ('id', 'name')


class WorkZoneMemberBaseSerializer(serializers.ModelSerializer):
    user = UserBaseSerializer(read_only=True, label="创建者")

    class Meta:
        model = WorkZoneMember
        fields = ('id', 'user', 'level')


class WorkZoneListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")
    permissions = serializers.SerializerMethodField(read_only=True)
    
    def get_permissions(self, obj):
        user = self.context['request'].user
        return get_work_zone_permission(user=user, work_zone=obj)
        
    class Meta:
        model = WorkZone
        fields = '__all__'


class WorkZoneDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")

    class Meta:
        model = WorkZone
        fields = '__all__'


class WorkZoneActionSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    creator = UserBaseSerializer(read_only=True, label="创建者")

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.creator = self.context['request'].user
        instance.save()
        WorkZoneMember.objects.get_or_create(work_zone=instance, user=instance.creator, level=ZONE_ADMIN)
        return instance

    class Meta:
        model = WorkZone
        fields = '__all__'

