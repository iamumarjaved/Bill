from django.urls import include,path
from rest_framework.routers import DefaultRouter
from riepilogo.views import RiepilogoViewSet

router = DefaultRouter()
router.register('riepilogo',RiepilogoViewSet,basename='riepilogo')

app_name = 'riepilogo'

urlpatterns = [
    path('',include(router.urls)),
    path('id/', RiepilogoViewSet.as_view({"get":"get_id"}), name='get-id'),
    ]