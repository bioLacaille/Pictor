from pictor.models import SampleSerialNumberSetting, ProjectSerialNumberSetting, AnalysisSerialNumberSetting, Sample, Project, Analysis


def get_sample_serial_number(add_num=1, work_zone=None):
    """获取系统生成的样本编号,  不存在配置则使用默认"""
    serial_number_setting = SampleSerialNumberSetting.objects.get_active(work_zone).first()
    if serial_number_setting:
        start_string = serial_number_setting.start_string
        middle_string_len = serial_number_setting.middle_string_len
        spilt_string = serial_number_setting.spilt_string
        end_string = serial_number_setting.end_string

    else:
        start_string = 'sample'
        middle_string_len = 6
        spilt_string = '-'
        end_string = ''
    count = Sample.objects.count() + add_num
    middle_string = str(count).zfill(int(middle_string_len))
    if spilt_string:
        serial_number = f'{start_string}{spilt_string}{middle_string}'
        if end_string:
            serial_number = f'{serial_number}{spilt_string}{end_string}'
    else:
        serial_number = f'{start_string}{middle_string}'
        if end_string:
            serial_number = f'{serial_number}{end_string}'
    return serial_number


def get_project_serial_number(add_num=1, work_zone=None):
    """获取系统生成的项目编号,  不存在配置则使用默认"""
    serial_number_setting = ProjectSerialNumberSetting.objects.get_active(work_zone).first()
    if serial_number_setting:
        start_string = serial_number_setting.start_string
        middle_string_len = serial_number_setting.middle_string_len
        spilt_string = serial_number_setting.spilt_string
        end_string = serial_number_setting.end_string

    else:
        start_string = 'project'
        middle_string_len = 6
        spilt_string = '-'
        end_string = ''
    count = Project.objects.count() + add_num
    middle_string = str(count).zfill(int(middle_string_len))
    if spilt_string:
        serial_number = f'{start_string}{spilt_string}{middle_string}'
        if end_string:
            serial_number = f'{serial_number}{spilt_string}{end_string}'
    else:
        serial_number = f'{start_string}{middle_string}'
        if end_string:
            serial_number = f'{serial_number}{end_string}'
    return serial_number


def get_analysis_serial_number(add_num=1, work_zone=None):
    """获取系统生成的分析编号,  不存在配置则使用默认"""
    serial_number_setting = AnalysisSerialNumberSetting.objects.get_active(work_zone).first()
    if serial_number_setting:
        start_string = serial_number_setting.start_string
        middle_string_len = serial_number_setting.middle_string_len
        spilt_string = serial_number_setting.spilt_string
        end_string = serial_number_setting.end_string

    else:
        start_string = 'analysis'
        middle_string_len = 6
        spilt_string = '-'
        end_string = ''
    count = Analysis.objects.count() + add_num
    middle_string = str(count).zfill(int(middle_string_len))
    if spilt_string:
        serial_number = f'{start_string}{spilt_string}{middle_string}'
        if end_string:
            serial_number = f'{serial_number}{spilt_string}{end_string}'
    else:
        serial_number = f'{start_string}{middle_string}'
        if end_string:
            serial_number = f'{serial_number}{end_string}'
    return serial_number

