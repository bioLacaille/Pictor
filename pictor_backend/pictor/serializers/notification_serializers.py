from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
import json
from pictor.models import Notification
from pictor.serializers.user_serializers import UserBaseSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """站内消息"""
    user = UserBaseSerializer(read_only=True, label='所属用户')
    content_object = serializers.SerializerMethodField(read_only=True, label='对象')
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='创建时间')

    def get_content_object(self, obj):
        if obj.content_object:
            content_type = ContentType.objects.get_for_model(obj.content_object)
            return {'id': obj.content_object.id, 'name': str(obj.content_object), 'model': content_type.model}
        else:
            return ''

    class Meta:
        model = Notification
        fields = '__all__'
