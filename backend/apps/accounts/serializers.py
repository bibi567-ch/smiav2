# apps/accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import UsuarioSMIA


class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email    = data.get('email')
        password = data.get('password')

        try:
            usuario = UsuarioSMIA.objects.get(email=email)
        except UsuarioSMIA.DoesNotExist:
            raise serializers.ValidationError(
                {'detail': 'Credenciales incorrectas.'}
            )

        # Verificar si está bloqueado
        if usuario.esta_bloqueado():
            raise serializers.ValidationError({
                'detail': 'Cuenta bloqueada temporalmente.',
                'bloqueado_hasta': usuario.bloqueado_hasta.isoformat(),
            })

        # Verificar contraseña
        if not usuario.check_password(password):
            usuario.registrar_intento_fallido()
            intentos_restantes = max(0, 3 - usuario.intentos_fallidos)
            raise serializers.ValidationError({
                'detail': 'Contraseña incorrecta.',
                'intentos_restantes': intentos_restantes,
            })

        # Login exitoso
        usuario.resetear_intentos()
        data['usuario'] = usuario
        return data


class UsuarioSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model  = UsuarioSMIA
        fields = ['id', 'email', 'nombres', 'apellidos',
                  'nombre_completo', 'rol']

    def get_nombre_completo(self, obj):
        return f'{obj.nombres} {obj.apellidos}'