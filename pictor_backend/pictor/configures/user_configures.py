"""
Author: Alan Fu
Email: fualan1990@gmail.com
用户模块所需配置
"""
USER = 10  # 业务菜单权限
SUPER_USER = 20  # 业务菜单权限+设置权限
ADMIN = 30  # 业务菜单权限+设置权限+管理权限
SUPER_ADMIN = 40  # 业务菜单权限+设置权限+管理权限+后期开发运维功能

ROLE_TYPE = {
    USER: 'user',
    SUPER_USER: 'super_user',
    ADMIN: 'admin',
    SUPER_ADMIN: 'super_admin',
}

ROLE_TYPE_ZH = {
    USER: '普通用户',
    SUPER_USER: '超级用户',
    ADMIN: '管理员',
    SUPER_ADMIN: '超级管理员',
}

ROLE_PERMISSIONS = {
    USER: ['user'],
    SUPER_USER: ['user', 'super_user'],
    ADMIN: ['user', 'super_user', 'admin'],
    SUPER_ADMIN: ['user', 'super_user', 'admin', 'super_admin'],
}