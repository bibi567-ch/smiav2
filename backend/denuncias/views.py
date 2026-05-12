from rest_framework import viewsets
from .models import DenunciaAmbiental
from .serializers import DenunciaSerializer

class DenunciaViewSet(viewsets.ModelViewSet):
    queryset = DenunciaAmbiental.objects.all()
    serializer_class = DenunciaSerializer