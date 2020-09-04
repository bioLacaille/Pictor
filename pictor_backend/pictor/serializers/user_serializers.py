from rest_framework import serializers
from pictor.models import User
from pictor.configures import ROLE_PERMISSIONS, ROLE_TYPE, ROLE_TYPE_ZH


class UserBaseSerializer(serializers.ModelSerializer):
    """用户序列化, 用于其他序列化当中"""
    avatar = serializers.SerializerMethodField(read_only=True)
    role = serializers.SerializerMethodField(read_only=True)

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return ''

    def get_role(self, obj):
        return ROLE_TYPE_ZH.get(obj.role_level, obj.role_level)

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'avatar', 'role', 'role_level')


class UserDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    last_login = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)
    role = serializers.SerializerMethodField(read_only=True)
    role_zh = serializers.SerializerMethodField(read_only=True)
    permissions = serializers.SerializerMethodField(read_only=True)

    def get_role(self, obj):
        return ROLE_TYPE.get(obj.role_level, obj.role_level)

    def get_role_zh(self, obj):
        return ROLE_TYPE_ZH.get(obj.role_level, obj.role_level)

    def get_permissions(self, obj):
        return ROLE_PERMISSIONS.get(obj.role_level, [])

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return ''

    class Meta:
        model = User
        exclude = ('password', 'is_deleted', 'groups', 'user_permissions')


class UserListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    role = serializers.SerializerMethodField(read_only=True)

    def get_role(self, obj):
        return ROLE_TYPE_ZH.get(obj.role_level, obj.role_level)

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email', 'phone', 'gender', 'title', 'is_active', 'role',
                  'role_level', 'created_time')


class UserActionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label='账号')
    password = serializers.CharField(label='密码', write_only=True, required=False)
    nickname = serializers.CharField(label='昵称')
    email = serializers.EmailField(label='邮箱')

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password(instance.password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'nickname', 'email', 'avatar', 'phone', 'gender', 'title',
                  'address', 'remark', 'role_level')

