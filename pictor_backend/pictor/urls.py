from django.conf.urls import url, include
from rest_framework import routers
from pictor.api import Authentication, ActionLogViewSet, NotificationRuleViewSet, NotificationViewSet, ProjectViewSet,\
    WorkZoneViewSet, UserViewSet, SampleViewSet, AnalysisModuleViewSet, DataSetViewSet, AnalysisViewSet, \
    AnalysisParameterViewSet, AnalysisTaskInterfaceViewSet, AnnouncementViewSet, \
    AnalysisSerialNumberSettingViewSet, ProjectSerialNumberSettingViewSet, SampleSerialNumberSettingViewSet, \
    StatisticViewSet
router_v1 = routers.DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('action_logs', ActionLogViewSet, basename='action_logs')
router_v1.register('notifications', NotificationViewSet, basename='notifications')

router_v1.register('projects', ProjectViewSet, basename='projects')
router_v1.register('work-zones', WorkZoneViewSet, basename='work_zones')
router_v1.register('samples', SampleViewSet, basename='samples')

router_v1.register('dataset', DataSetViewSet, basename='dataset')
router_v1.register('analysis', AnalysisViewSet, basename='analysis')

router_v1.register('statistic', StatisticViewSet, basename='statistic')

router_v1.register('analysis_nums', AnalysisSerialNumberSettingViewSet, basename='analysis_nums')
router_v1.register('project_nums', ProjectSerialNumberSettingViewSet, basename='project_nums')
router_v1.register('sample_nums', SampleSerialNumberSettingViewSet, basename='sample_nums')

router_v1.register('analysis_modules', AnalysisModuleViewSet, basename='analysis_modules')
router_v1.register('analysis_parameters', AnalysisParameterViewSet, basename='analysis_parameters')
router_v1.register('analysis_task_interface', AnalysisTaskInterfaceViewSet, basename='analysis_task_interface')
router_v1.register('notification_rules', NotificationRuleViewSet, basename='notification_rules')
router_v1.register('announcements', AnnouncementViewSet, basename='announcements')

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router_v1.urls), name='api-index'),
    url(r'^auth/$', Authentication.as_view(), name='authentication'),
]
