from django.conf.urls import url, include
from rest_framework import routers
from fake_api.views import AnalysisTaskViewSet
router_fake = routers.DefaultRouter()

router_fake.register('analysis_tasks', AnalysisTaskViewSet, basename='analysis_tasks')

urlpatterns = [
    url(r'^', include(router_fake.urls), name='api-fake'),
]
