# apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioSMIA

@admin.register(UsuarioSMIA)
class UsuarioSMIAAdmin(UserAdmin):
    list_display    = ('email', 'nombres', 'apellidos', 'rol', 'is_active')
    list_filter     = ('rol', 'is_active')
    search_fields   = ('email', 'nombres', 'apellidos')
    ordering        = ('email',)
    fieldsets       = (
        (None,          {'fields': ('email', 'password')}),
        ('Datos',       {'fields': ('nombres', 'apellidos', 'rol')}),
        ('Permisos',    {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets   = (
        (None, {
            'classes': ('wide',),
            'fields':  ('email', 'nombres', 'apellidos', 'rol', 'password1', 'password2'),
        }),
    )