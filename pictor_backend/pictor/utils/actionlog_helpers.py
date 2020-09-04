from pictor.configures import DELETE_ACTION_TYPE, BULK_DELETE_ACTION_TYPE
from pictor.models import ActionLog
from datetime import datetime
from pictor.utils.applog_helpers import api_logger
import json


def model_to_dic(instance):
    if instance:
        _instance = {}
        # 当前模型除了多对多的所有字段
        for field in instance._meta.fields:
            # field_type = field.get_internal_type()
            field_name = field.name
            key = getattr(field, '_verbose_name', field_name)
            value = getattr(instance, field_name, None)

            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            _instance[key] = str(value)
        # todo 记录多对多
        # 多对多关系由第三张表记录，当前实例修改了多对多记录，旧实例进行多对多查询时只能查到最新记录。故多对多操作无法记录
        # for field in instance._meta.many_to_many:
        #     field_name = field.name
        #     query = getattr(instance, field_name)
        #     # query.all() 旧实例查询第三张表，查询结果为最新条件无法记录
        #     _instance[field_name] = {obj.id: str(obj) for obj in query.all()}
        return _instance
    return {}


def diff_model_instance(old_instance=None, instance=None):
    # 将模型转化为字典
    old_instance = model_to_dic(old_instance)
    instance = model_to_dic(instance)
    fields = old_instance.keys() if old_instance else instance.keys()
    # 对比两个对象差异
    change = dict()
    for field in fields:
        old_value = old_instance.get(field)
        new_value = instance.get(field)
        if old_value != new_value:
            change[field] = [old_value, new_value]
    for field in ['password', 'last login']:
        if field in change:
            change.pop(field)
    try:
        change = json.dumps(change, ensure_ascii=False)
    except Exception as e:
        api_logger.error(f'json.dumps err ->', e)
        api_logger.error(f'changes ->', change)
        change = {}
    return change


def action_log(request, user, action_type, old_instance=None, instance=None, action_info="", object_changes=None):
    # 批量操作，可以先实例化日志对象，在进行bulk_create操作
    # 日志记录
    try:
        # 取出操作请求，从其中得到ip地址
        if request is not None:
            x_real_ip = request.META.get('HTTP_X_REAL_IP')
            if x_real_ip:
                remote_ip = x_real_ip.split(',')[0]
            else:
                http_remote_ip = request.META.get('HTTP_REMOTE_ADDR')
                if http_remote_ip:
                    remote_ip = http_remote_ip.split(',')[0]
                else:
                    remote_ip = request.META.get('REMOTE_ADDR')
        else:
            remote_ip = None
        # 如果instance存在日记记录对象为instance，否则为old_instance
        content_object = instance if instance else old_instance
        if old_instance and instance:
            object_changes = diff_model_instance(old_instance, instance)
        elif action_type in [DELETE_ACTION_TYPE, BULK_DELETE_ACTION_TYPE]:
            # old_instance -> content_object
            object_changes = diff_model_instance(content_object, None)
        ActionLog.objects.create(content_object=content_object, user=user, action_type=action_type,
                                 action_info=action_info, object_changes=object_changes, remote_ip=remote_ip)
        api_logger.debug(f'记录日志信息:{remote_ip}-{content_object}-{user}-{action_type}-{action_info}-{object_changes}')
    except Exception as error:
        api_logger.error("日志记录过程中发生错误, 具体错误:{}".format(error))
