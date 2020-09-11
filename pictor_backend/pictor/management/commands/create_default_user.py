from pictor.models import User
from django.core.management.base import BaseCommand, CommandError
import random


class Command(BaseCommand):
    help = 'Initial Data for System'

    def add_arguments(self, parser):
        # parser.add_argument('arg', nargs='+', type=int)
        pass

    def create_system_user(self, username, email, nickname, password, role_level, **kwargs):
        system_user = User.objects.filter(username=username).first()
        if system_user:
            self.stdout.write(self.style.SUCCESS(f'user :{username} exist'))
        else:
            self.stdout.write(self.style.SUCCESS(f'create user:{username}'))
            system_user = User.objects.create_superuser(username=username, email=email, nickname=nickname,
                                                        password=password, role_level=role_level, **kwargs)
        return system_user

    def handle(self, *args, **options):
        # 创建用户
        self.create_system_user(username='super_admin', email='super_admin@pictor.com.cn', nickname='超级管理员',
                                password='pictor123456', role_level=40, phone='13533032222', title='全栈开发工程师')
        self.create_system_user(username='admin', email='admin@pictor.com.cn', nickname='管理员',
                                password='pictor123456', role_level=30, phone='13533032222', title='全栈开发工程师')
        self.create_system_user(username='super_user', email='super_user@pictor.com.cn', nickname='超级用户',
                                password='pictor123456', role_level=20, phone='13533032222', title='全栈开发工程师')
        self.create_system_user(username='user', email='user@pictor.com.cn', nickname='普通用户',
                                password='pictor123456', role_level=10, phone='13533032222', title='全栈开发工程师')
        self.create_system_user(username='alan', email='fualan1990@gmail.com', nickname='司马扶妖',
                                password='fu030632', role_level=40, phone='13533032222', title='全栈开发工程师')