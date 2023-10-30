from rest_framework import viewsets,mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiParameter
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.http import HttpResponse
from django.http import FileResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from core.models import DownloadRequest
from download.serializers import DownloadSerializer
import os


class DownloadViewSet(viewsets.GenericViewSet,mixins.ListModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DownloadSerializer
    queryset = DownloadRequest.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(name='unique_id',location=OpenApiParameter.QUERY, description='Unique ID', required=True, type=str),
        ],
    )
    @action(detail=False, methods=['get'])
    def download_complete(self, request):
        unique_id = request.GET.get('unique_id', '')
        try:
            result = DownloadRequest.objects.get(unique_id=unique_id)
        except ObjectDoesNotExist:
            return HttpResponse("Unique ID not present.")
        if result.unique_id:
            file_name = f'generated_file_{unique_id}.csv'
            file_path = os.path.join(settings.DYNAMIC_FILES,'generated', file_name)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'rb') as file:
                        response = HttpResponse(file, content_type='text/csv')
                        response['Content-Disposition'] = f'attachment; filename={file_name}'
                        return response
                except FileNotFoundError:
                    return HttpResponse("Error reading file.")
            else:
                return HttpResponse("File not found.")
        else:
            return HttpResponse("Unique ID not provided.")
