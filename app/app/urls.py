"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(),name='api-schema'),
    path('api/docs/',SpectacularSwaggerView.as_view(url_name='api-schema'),name='api-docs'),
    path('api/historic/',include("historic.urls")),
    path('api/user/',include("user.urls")),
    path('api/download/',include('download.urls')),
    path('api/riepilogo/',include('riepilogo.urls')),
    re_path(r'^virgiliotms/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT + '/ui'}),
]
