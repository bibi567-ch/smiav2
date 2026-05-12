# apps/accounts/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone


class RolSistema(models.TextChoices):
    ADMIN            = 'ADMIN',        'Administrador del Sistema'
    DIRECTOR         = 'DIRECTOR',     'Director SMGA'
    TECNICO_AIRE     = 'TECNICO_AIRE', 'Técnico Calidad del Aire'
    TECNICO_AGUA     = 'TECNICO_AGUA', 'Técnico Calidad del Agua'
    TECNICO_RESIDUOS = 'TECNICO_RES',  'Técnico Gestión de Residuos'
    TECNICO_RUIDO    = 'TECNICO_RUIDO','Técnico Control de Ruido'
    TECNICO_VEH      = 'TECNICO_VEH',  'Técnico Emisiones Vehiculares'
    AUDITOR          = 'AUDITOR',      'Auditor ASDI/Helvetas'
    CIUDADANO        = 'CIUDADANO',    'Ciudadano La Paz'


class UsuarioSMIAManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('rol', RolSistema.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class UsuarioSMIA(AbstractBaseUser, PermissionsMixin):
    email             = models.EmailField(unique=True)
    nombres           = models.CharField(max_length=150)
    apellidos         = models.CharField(max_length=150)
    rol               = models.CharField(
                            max_length=20,
                            choices=RolSistema.choices,
                            default=RolSistema.CIUDADANO
                        )
    intentos_fallidos = models.PositiveSmallIntegerField(default=0)
    bloqueado_hasta   = models.DateTimeField(null=True, blank=True)
    is_active         = models.BooleanField(default=True)
    is_staff          = models.BooleanField(default=False)
    fecha_creacion    = models.DateTimeField(auto_now_add=True)

    objects = UsuarioSMIAManager()
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['nombres', 'apellidos']

    class Meta:
        db_table = 'smia_usuarios'

    def __str__(self):
        return f'{self.nombres} {self.apellidos} ({self.rol})'

    def esta_bloqueado(self):
        if self.bloqueado_hasta and timezone.now() < self.bloqueado_hasta:
            return True
        return False

    def registrar_intento_fallido(self):
        self.intentos_fallidos += 1
        if self.intentos_fallidos >= 3:
            self.bloqueado_hasta = timezone.now() + timezone.timedelta(minutes=15)
        self.save(update_fields=['intentos_fallidos', 'bloqueado_hasta'])

    def resetear_intentos(self):
        self.intentos_fallidos = 0
        self.bloqueado_hasta   = None
        self.save(update_fields=['intentos_fallidos', 'bloqueado_hasta'])