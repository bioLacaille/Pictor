"""
Author: Alan Fu
Email: fualan1990@gmail.com
统计API接口
"""
from rest_framework import viewsets, mixins, filters, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from pictor.models import Project, Sample, Analysis, WorkZone


class StatisticViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        query_params = self.request.query_params
        work_zone_id = query_params.get('work_zone', "")
        try:
            work_zone = WorkZone.objects.get(pk=int(work_zone_id))
        except:
            work_zone = None
        if work_zone:
            project_count = Project.objects.filter(work_zone=work_zone).count()
            sample_count = Sample.objects.filter(work_zone=work_zone).count()
            analysis_count = Analysis.objects.filter(work_zone=work_zone).count()
        else:
            project_count = Project.objects.count()
            sample_count = Sample.objects.count()
            analysis_count = Analysis.objects.count()
        result = {'success': True, 'messages': '当前数据量!',
                  'results': {
                      'project_count': project_count,
                      'sample_count': sample_count,
                      'analysis_count': analysis_count,
                  }}
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def test(self, request, *args, **kwargs):
        result = {'success': True, 'messages': f'test!', 'results': {}}
        return Response(result, status=status.HTTP_200_OK)
