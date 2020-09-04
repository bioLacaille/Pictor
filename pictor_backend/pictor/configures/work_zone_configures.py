"""
Author: Alan Fu
Email: fualan1990@gmail.com
工作区模块所需配置
"""
ZONE_GUEST = 10  # 仅拥有查看权限
ZONE_USER = 20  # 通用权限(新增/修改/查询/以及一般操作)
ZONE_MAINTAINER = 30  # 通用权限+危险操作(删除)
ZONE_ADMIN = 40  # 拥有者, 所有权限

MEMBER_TYPE = {
    ZONE_GUEST: 'guest',
    ZONE_USER: 'user',
    ZONE_MAINTAINER: 'maintainer',
    ZONE_ADMIN: 'admin',
}

MEMBER_TYPE_ZH = {
    ZONE_GUEST: '工作区游客',
    ZONE_USER: '工作区普通成员',
    ZONE_MAINTAINER: '工作区超级成员',
    ZONE_ADMIN: '工作区管理员',
}