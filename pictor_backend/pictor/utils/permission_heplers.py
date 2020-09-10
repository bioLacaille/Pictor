from pictor.configures.permission_configures import *
from pictor.configures import ADMIN, ZONE_ADMIN, ZONE_MAINTAINER, ZONE_USER
from pictor.models import WorkZoneMember


def get_work_zone_permission(user, work_zone=None):
    """
    获取工作区的操作权限,
    系统管理员与超级管理员可操作关于工作区的任意功能
    工作区游客仅能查看
    工作区普通成员与工作区超级成员可编辑
    工作区管理员可操作关于工作区的任意功能
    :param user: 
    :param work_zone: 
    :return: 
    """
    perm = WORK_ZONE_PERMISSION.copy()
    if user.role_level >= ADMIN:
        for key, value in perm.items():
            perm[key] = True
    elif work_zone:
        work_zone_member = WorkZoneMember.objects.filter(work_zone=work_zone, user=user).first()
        if work_zone_member and work_zone_member.level == ZONE_USER:
            perm['edit'] = True
        if work_zone_member and work_zone_member.level == ZONE_MAINTAINER:
            perm['edit'] = True
        if work_zone_member and work_zone_member.level == ZONE_ADMIN:
            for key, value in perm.items():
                perm[key] = True
    return perm


def get_project_permission(user, work_zone=None):
    """
    获取项目的操作权限,
    系统管理员与超级管理员可操作关于工作区的任意功能
    工作区游客仅能查看
    工作区普通成员与工作区超级成员可编辑
    工作区管理员可操作关于工作区的任意功能
    :param user:
    :param work_zone:
    :return:
    """
    perm = PROJECT_PERMISSION.copy()
    if user.role_level >= ADMIN:
        for key, value in perm.items():
            perm[key] = True
    elif work_zone:
        work_zone_member = WorkZoneMember.objects.filter(work_zone=work_zone, user=user).first()
        if work_zone_member and work_zone_member.level == ZONE_USER:
            perm['add'] = True
            perm['edit'] = True
            perm['manage'] = True
        if work_zone_member and work_zone_member.level == ZONE_MAINTAINER:
            perm['add'] = True
            perm['edit'] = True
            perm['manage'] = True
        if work_zone_member and work_zone_member.level == ZONE_ADMIN:
            for key, value in perm.items():
                perm[key] = True
    return perm


def get_sample_permission(user, work_zone=None):
    """
    获取样本的操作权限,
    系统管理员与超级管理员可操作关于工作区的任意功能
    工作区游客仅能查看
    工作区普通成员与工作区超级成员可编辑
    工作区管理员可操作关于工作区的任意功能
    :param user:
    :param work_zone:
    :return:
    """
    perm = SAMPLE_PERMISSION.copy()
    if user.role_level >= ADMIN:
        for key, value in perm.items():
            perm[key] = True
    elif work_zone:
        work_zone_member = WorkZoneMember.objects.filter(work_zone=work_zone, user=user).first()
        if work_zone_member and work_zone_member.level == ZONE_USER:
            perm['add'] = True
            perm['edit'] = True
        if work_zone_member and work_zone_member.level == ZONE_MAINTAINER:
            perm['add'] = True
            perm['edit'] = True
            perm['delete'] = True
        if work_zone_member and work_zone_member.level == ZONE_ADMIN:
            for key, value in perm.items():
                perm[key] = True
    return perm


def get_dataset_permission(user, work_zone=None):
    """
    获取数据集的操作权限,
    """
    perm = DATASET_PERMISSION.copy()
    if user.role_level >= ADMIN:
        for key, value in perm.items():
            perm[key] = True
    elif work_zone:
        work_zone_member = WorkZoneMember.objects.filter(work_zone=work_zone, user=user).first()
        if work_zone_member and work_zone_member.level == ZONE_USER:
            perm['upload'] = True
            perm['create_directory'] = True
        if work_zone_member and work_zone_member.level == ZONE_MAINTAINER:
            perm['upload'] = True
            perm['create_directory'] = True
            perm['delete'] = True
            perm['download'] = True
            perm['rename'] = True
            perm['copy'] = True
            perm['move'] = True
        if work_zone_member and work_zone_member.level == ZONE_ADMIN:
            for key, value in perm.items():
                perm[key] = True
    return perm


def get_analysis_permission(user, work_zone=None):
    """
    获取分析任务的操作权限,
    """
    perm = ANALYSIS_PERMISSION.copy()
    if user.role_level >= ADMIN:
        for key, value in perm.items():
            perm[key] = True
    elif work_zone:
        work_zone_member = WorkZoneMember.objects.filter(work_zone=work_zone, user=user).first()
        if work_zone_member and work_zone_member.level == ZONE_USER:
            perm['add'] = True
            perm['edit'] = True
        if work_zone_member and work_zone_member.level == ZONE_MAINTAINER:
            perm['add'] = True
            perm['edit'] = True
            perm['delete'] = True
            perm['start'] = True
            perm['stop'] = True
            perm['continue'] = True
            perm['reset'] = True
        if work_zone_member and work_zone_member.level == ZONE_ADMIN:
            for key, value in perm.items():
                perm[key] = True
    return perm


def get_num_set_permission(user, work_zone=None):
    """
    获取编号设置的操作权限,
    """
    perm = NUMBER_SETTING_PERMISSION.copy()
    if user.role_level >= ADMIN:
        for key, value in perm.items():
            perm[key] = True
    elif work_zone:
        work_zone_member = WorkZoneMember.objects.filter(work_zone=work_zone, user=user).first()
        if work_zone_member and work_zone_member.level == ZONE_USER:
            perm['add'] = True
            perm['edit'] = True
        if work_zone_member and work_zone_member.level == ZONE_MAINTAINER:
            perm['add'] = True
            perm['edit'] = True
            perm['delete'] = True
            perm['active'] = True
        if work_zone_member and work_zone_member.level == ZONE_ADMIN:
            for key, value in perm.items():
                perm[key] = True
    return perm