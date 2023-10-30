from django.urls import path,include
from rest_framework.routers import DefaultRouter

from download import views

router = DefaultRouter()
router.register('',views.DownloadViewSet)

app_name = 'download'

urlpatterns = [
    path('',include(router.urls))
    ]