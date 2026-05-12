from django.contrib import admin
from .models import (
    PuntoMonitoreo, EstacionAire, MuestraAire,
    PuntoAgua, MuestraAgua
)

@admin.register(PuntoMonitoreo)
class PuntoMonitoreoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'activo')
    list_filter = ('tipo', 'activo')

@admin.register(EstacionAire)
class EstacionAireAdmin(admin.ModelAdmin):
    list_display = ('codigo_monica', 'punto', 'tipo_estacion')

@admin.register(MuestraAire)
class MuestraAireAdmin(admin.ModelAdmin):
    list_display = ('estacion', 'fecha_hora', 'ica_valor', 'ica_nivel')
    readonly_fields = ('ica_valor', 'ica_nivel', 'ica_contaminante_critico')

@admin.register(PuntoAgua)
class PuntoAguaAdmin(admin.ModelAdmin):
    list_display = ('punto', 'tipo_cuerpo', 'cuenca')

@admin.register(MuestraAgua)
class MuestraAguaAdmin(admin.ModelAdmin):
    list_display = ('punto_agua', 'fecha_hora', 'cumple_ley')
    readonly_fields = ('cumple_ley', 'parametros_excedidos')