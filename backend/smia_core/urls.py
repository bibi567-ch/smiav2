# smia_core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',          admin.site.urls),
    path('api/auth/',       include('apps.accounts.urls')),
    path('api/monitoreo/',  include('apps.monitoreo.urls')),
    path('api/denuncias/',  include('denuncias.urls')),
]