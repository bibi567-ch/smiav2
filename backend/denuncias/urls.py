from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DenunciaViewSet

router = DefaultRouter()
# Lo dejamos vacío ('') porque el archivo principal ya le pone 'api/denuncias/'
router.register(r'', DenunciaViewSet, basename='denuncia')

urlpatterns = [
    path('', include(router.urls)),
]