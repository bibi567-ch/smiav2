# apps/accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UsuarioSerializer


class LoginView(APIView):
    """
    POST /api/auth/login/
    Retorna access + refresh token y datos del usuario.
    Cumple: HU-01.1, RF-01
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_401_UNAUTHORIZED
            )

        usuario = serializer.validated_data['usuario']
        refresh = RefreshToken.for_user(usuario)

        return Response({
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
            'usuario': UsuarioSerializer(usuario).data,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Invalida el refresh token (blacklist).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'detail': 'Sesión cerrada correctamente.'},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {'detail': 'Token inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class PerfilView(APIView):
    """GET /api/auth/perfil/ — Datos del usuario autenticado."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UsuarioSerializer(request.user).data)