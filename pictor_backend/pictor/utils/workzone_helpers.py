from pictor.models import Project, Sample, DataSet, Sequencing, Analysis, \
    AnalysisSerialNumberSetting, SampleSerialNumberSetting, SequencingSerialNumberSetting, ProjectSerialNumberSetting, \
    FileUploadSetting


def transfer_work_zone_record(instance, transfer_target):
    projects = Project.objects.filter(work_zone=instance).all()
    samples = Sample.objects.filter(work_zone=instance).all()
    dataset = DataSet.objects.filter(work_zone=instance).all()
    sequencing = Sequencing.objects.filter(work_zone=instance).all()
    analysis = Analysis.objects.filter(work_zone=instance).all()
    file_upload_setting = FileUploadSetting.objects.filter(work_zone=instance).all()
    sample_number_setting = SampleSerialNumberSetting.objects.filter(work_zone=instance).all()
    project_number_setting = ProjectSerialNumberSetting.objects.filter(work_zone=instance).all()
    sequencing_number_setting = SequencingSerialNumberSetting.objects.filter(work_zone=instance).all()
    analysis_number_setting = AnalysisSerialNumberSetting.objects.filter(work_zone=instance).all()
    try:
        projects.update(work_zone=transfer_target)
        samples.update(work_zone=transfer_target)
        dataset.update(work_zone=transfer_target)
        sequencing.update(work_zone=transfer_target)
        analysis.update(work_zone=transfer_target)
        file_upload_setting.update(work_zone=transfer_target)
        sample_number_setting.update(work_zone=transfer_target)
        project_number_setting.update(work_zone=transfer_target)
        sequencing_number_setting.update(work_zone=transfer_target)
        analysis_number_setting.update(work_zone=transfer_target)
    except Exception as error:
        projects.update(work_zone=instance)
        samples.update(work_zone=instance)
        dataset.update(work_zone=instance)
        sequencing.update(work_zone=instance)
        analysis.update(work_zone=instance)
        file_upload_setting.update(work_zone=instance)
        sample_number_setting.update(work_zone=instance)
        project_number_setting.update(work_zone=instance)
        sequencing_number_setting.update(work_zone=instance)
        analysis_number_setting.update(work_zone=instance)