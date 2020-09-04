"""
Author: Alan Fu
Email: fualan1990@gmail.com
用户数据模块
"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from pictor.configures import ROLE_TYPE, ROLE_TYPE_ZH, SUPER_ADMIN, USER
from pictor.utils.base_heplers import change_dict_for_model_choices


# 上传文件目录
def upload_avatar_path(instance, filename):
    file_path = 'avatar/{username}/{filename}'.format(
        username=instance.username,
        filename=filename
    )
    return file_path


class UserManager(BaseUserManager):
    """
    用户管理
    """
    def create_user(self, username, password, **extra_fields):
        # username 是唯一标识，没有会报错
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)  # 检测密码合理性
        user.save(using=self._db)  # 保存密码
        return user

    def create_superuser(self, username, password, **extra_fields):
        user = self.create_user(username=username,
                                password=password, **extra_fields)
        user.role_level = SUPER_ADMIN  # 比创建用户多的一个字段
        user.is_superuser = True  # permission 中的字段
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """用户"""
    username = models.CharField(max_length=255, unique=True, db_index=True, verbose_name='帐号')
    nickname = models.CharField(max_length=255, verbose_name='昵称')
    email = models.EmailField(max_length=255, verbose_name='邮箱')
    avatar = models.ImageField(default='avatar/default_avatar.jpg', upload_to=upload_avatar_path, blank=True, null=True, verbose_name='头像')
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name='手机号码')
    gender = models.CharField(max_length=10, default='男', null=True, blank=True, verbose_name='性别')
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='岗位职称')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='地址')
    remark = models.TextField(null=True, blank=True, verbose_name='简介/备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建日期')
    is_deleted = models.BooleanField(default=False, verbose_name='是否已经删除')
    is_active = models.BooleanField(default=True, verbose_name='是否可用')
    role_level = models.IntegerField(default=USER, choices=change_dict_for_model_choices(ROLE_TYPE), verbose_name='用户等级')
    USERNAME_FIELD = 'username'  # 必须有一个唯一标识--USERNAME_FIELD
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.username
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nickname}({self.username})'

    @property
    def is_staff(self):
        if self.role_level >= SUPER_ADMIN:
            return True
        else:
            return False

    @property
    def role(self):
        return ROLE_TYPE.get(self.role_level, '')

    @property
    def role_zh(self):
        return ROLE_TYPE_ZH.get(self.role_level, '')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    objects = UserManager()
