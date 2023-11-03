"""
URL mappings for historic API.
"""

from django.urls import path,include

from rest_framework.routers import DefaultRouter

from historic import views


router = DefaultRouter()
router.register('historic', views.HistoricViewSet,basename='download')

app_name = 'historic' #name for reverse url

urlpatterns = [
    path('',include(router.urls)),
]