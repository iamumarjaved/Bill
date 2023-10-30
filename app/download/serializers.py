from rest_framework.serializers import ModelSerializer
from core.models import DownloadRequest

class DownloadSerializer(ModelSerializer):
    class Meta:
        model = DownloadRequest
        fields = '__all__'