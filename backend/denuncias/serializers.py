from rest_framework import serializers
from .models import DenunciaAmbiental

class DenunciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DenunciaAmbiental
        fields = '__all__'  # Esto traduce todos los campos automáticamente