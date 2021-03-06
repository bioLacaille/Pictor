"""
author: Alan Fu
基础共用方法
"""
import os


def change_list_for_model_choices(value_list):
    # 将列表转为数据模型可用选项
    return ((value, value) for value in value_list)


def change_dict_for_model_choices(value_dict):
    # 将字典转换未数据模型可用选项
    return ((key, value) for key, value in value_dict.items())


def create_or_get_directory(directory_path):
    # 若目录不存在则创建
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    return directory_path


def check_model_field(model, field_name, field_ype):
    # 检查当前外键盘是否具体类型
    try:
        field_object = model._meta.get_field(field_name)
        if isinstance(field_object, field_ype):
            return field_object
        else:
            return None
    except:
        return None

