from django.urls import path
from .views import LoginView, LogoutView, PerfilView

urlpatterns = [
    path('login/',  LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('perfil/', PerfilView.as_view()),
]
# La URL final correcta será: /api/auth/login/