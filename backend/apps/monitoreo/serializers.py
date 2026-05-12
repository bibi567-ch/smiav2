# apps/monitoreo/serializers.py
"""
Serializers (DTOs) del módulo de monitoreo.
Filtran y formatean los datos que se exponen a Angular.
Cumple: Patrón DTO, RF-04, RF-05
"""
from rest_framework import serializers
from .models import (
    PuntoMonitoreo, EstacionAire, MuestraAire,
    PuntoAgua, MuestraAgua,
    PuntoResiduos, PesajeResiduos,
    MedicionRuido, MedicionVehicular
)
from .calculadora_ica import calcular_ica, verificar_cumplimiento_agua


# ── Puntos de monitoreo ──────────────────────────────────────────────

class PuntoMonitoreoSerializer(serializers.ModelSerializer):
    """Serializer base para mapa — incluye coordenadas y tipo."""
    tipo_display = serializers.CharField(
        source='get_tipo_display', read_only=True
    )

    class Meta:
        model  = PuntoMonitoreo
        fields = [
            'id', 'nombre', 'tipo', 'tipo_display',
            'latitud', 'longitud', 'descripcion', 'activo'
        ]


# ── Estación de Aire ─────────────────────────────────────────────────

class EstacionAireSerializer(serializers.ModelSerializer):
    punto = PuntoMonitoreoSerializer(read_only=True)

    class Meta:
        model  = EstacionAire
        fields = ['id', 'punto', 'tipo_estacion', 'codigo_monica']


class EstacionAireCreateSerializer(serializers.ModelSerializer):
    """Para crear una estación con su punto de monitoreo."""
    nombre      = serializers.CharField(write_only=True)
    latitud     = serializers.DecimalField(
                    max_digits=10, decimal_places=7, write_only=True
                  )
    longitud    = serializers.DecimalField(
                    max_digits=10, decimal_places=7, write_only=True
                  )
    descripcion = serializers.CharField(
                    required=False, allow_blank=True, write_only=True
                  )

    class Meta:
        model  = EstacionAire
        fields = [
            'nombre', 'latitud', 'longitud', 'descripcion',
            'tipo_estacion', 'codigo_monica'
        ]

    def create(self, validated_data):
        request = self.context['request']
        punto = PuntoMonitoreo.objects.create(
            nombre      = validated_data.pop('nombre'),
            tipo        = 'AIRE',
            latitud     = validated_data.pop('latitud'),
            longitud    = validated_data.pop('longitud'),
            descripcion = validated_data.pop('descripcion', ''),
            creado_por  = request.user,
        )
        return EstacionAire.objects.create(punto=punto, **validated_data)


# ── Muestra de Aire ──────────────────────────────────────────────────

class MuestraAireSerializer(serializers.ModelSerializer):
    estacion_nombre = serializers.CharField(
        source='estacion.punto.nombre', read_only=True
    )
    nivel_display = serializers.CharField(
        source='get_ica_nivel_display', read_only=True
    )

    class Meta:
        model  = MuestraAire
        fields = [
            'id', 'estacion', 'estacion_nombre', 'fecha_hora',
            'pm25', 'pm10', 'no2', 'so2', 'co', 'o3',
            'ica_valor', 'ica_nivel', 'nivel_display',
            'ica_contaminante_critico',
        ]
        read_only_fields = ['ica_valor', 'ica_nivel', 'ica_contaminante_critico']

    def create(self, validated_data):
        """Calcula el ICA automáticamente antes de guardar."""
        resultado = calcular_ica(
            pm25 = float(validated_data.get('pm25') or 0) or None,
            pm10 = float(validated_data.get('pm10') or 0) or None,
            no2  = float(validated_data.get('no2')  or 0) or None,
            so2  = float(validated_data.get('so2')  or 0) or None,
            co   = float(validated_data.get('co')   or 0) or None,
            o3   = float(validated_data.get('o3')   or 0) or None,
        )
        validated_data['ica_valor']                = resultado.valor
        validated_data['ica_nivel']                = resultado.nivel
        validated_data['ica_contaminante_critico'] = resultado.contaminante_critico
        validated_data['registrado_por']           = self.context['request'].user
        return super().create(validated_data)


# ── Punto de Agua ────────────────────────────────────────────────────

class PuntoAguaSerializer(serializers.ModelSerializer):
    punto = PuntoMonitoreoSerializer(read_only=True)

    class Meta:
        model  = PuntoAgua
        fields = ['id', 'punto', 'tipo_cuerpo', 'cuenca']


class PuntoAguaCreateSerializer(serializers.ModelSerializer):
    nombre   = serializers.CharField(write_only=True)
    latitud  = serializers.DecimalField(max_digits=10, decimal_places=7, write_only=True)
    longitud = serializers.DecimalField(max_digits=10, decimal_places=7, write_only=True)

    class Meta:
        model  = PuntoAgua
        fields = ['nombre', 'latitud', 'longitud', 'tipo_cuerpo', 'cuenca']

    def create(self, validated_data):
        request = self.context['request']
        punto = PuntoMonitoreo.objects.create(
            nombre     = validated_data.pop('nombre'),
            tipo       = 'AGUA',
            latitud    = validated_data.pop('latitud'),
            longitud   = validated_data.pop('longitud'),
            creado_por = request.user,
        )
        return PuntoAgua.objects.create(punto=punto, **validated_data)


# ── Muestra de Agua ──────────────────────────────────────────────────

class MuestraAguaSerializer(serializers.ModelSerializer):
    punto_nombre = serializers.CharField(
        source='punto_agua.punto.nombre', read_only=True
    )

    class Meta:
        model  = MuestraAgua
        fields = [
            'id', 'punto_agua', 'punto_nombre', 'fecha_hora',
            'ph', 'dbo', 'dqo', 'coliformes', 'turbidez', 'temperatura',
            'cumple_ley', 'parametros_excedidos',
        ]
        read_only_fields = ['cumple_ley', 'parametros_excedidos']

    def create(self, validated_data):
        """Verifica automáticamente cumplimiento Ley N°1333."""
        cumple, excedidos = verificar_cumplimiento_agua(validated_data)
        validated_data['cumple_ley']           = cumple
        validated_data['parametros_excedidos'] = excedidos
        validated_data['registrado_por']       = self.context['request'].user
        return super().create(validated_data)


# ── Pesaje de Residuos ───────────────────────────────────────────────

class PesajeResiduosSerializer(serializers.ModelSerializer):
    punto_nombre    = serializers.CharField(
        source='punto_residuos.punto.nombre', read_only=True
    )
    sigir_estado_display = serializers.CharField(
        source='get_sigir_estado_display', read_only=True
    )

    class Meta:
        model  = PesajeResiduos
        fields = [
            'id', 'punto_residuos', 'punto_nombre', 'fecha',
            'tipo_residuo', 'peso_toneladas', 'operador',
            'sigir_estado', 'sigir_estado_display', 'sigir_timestamp',
        ]
        read_only_fields = ['sigir_estado', 'sigir_timestamp']

    def create(self, validated_data):
        validated_data['registrado_por'] = self.context['request'].user
        return super().create(validated_data)


# ── Medición de Ruido ────────────────────────────────────────────────

class MedicionRuidoSerializer(serializers.ModelSerializer):
    punto_nombre  = serializers.CharField(
        source='punto.nombre', read_only=True
    )
    zona_display  = serializers.CharField(
        source='get_zona_display', read_only=True
    )

    class Meta:
        model  = MedicionRuido
        fields = [
            'id', 'punto', 'punto_nombre', 'fecha_hora',
            'zona', 'zona_display', 'nivel_db',
            'es_nocturno', 'es_excedencia', 'observaciones',
        ]
        read_only_fields = ['es_excedencia']

    def create(self, validated_data):
        """Calcula automáticamente si hay excedencia."""
        zona        = validated_data.get('zona', 'RESIDENCIAL')
        nivel_db    = float(validated_data.get('nivel_db', 0))
        es_nocturno = validated_data.get('es_nocturno', False)
        turno       = 'nocturno' if es_nocturno else 'diurno'

        limites = MedicionRuido.LIMITES_ZONA.get(zona, {})
        limite  = limites.get(turno, 65)
        validated_data['es_excedencia']  = nivel_db > limite
        validated_data['registrado_por'] = self.context['request'].user
        return super().create(validated_data)


# ── Medición Vehicular ───────────────────────────────────────────────

class MedicionVehicularSerializer(serializers.ModelSerializer):
    punto_nombre = serializers.CharField(
        source='punto.nombre', read_only=True
    )

    class Meta:
        model  = MedicionVehicular
        fields = [
            'id', 'punto', 'punto_nombre', 'fecha_hora',
            'placa', 'tipo_vehiculo', 'anio_vehiculo',
            'co_pct', 'hc_ppm', 'nox_ppm', 'opacidad_pct',
            'cumple_norma',
        ]

    def create(self, validated_data):
        validated_data['registrado_por'] = self.context['request'].user
        return super().create(validated_data)


# ── Serializer del Mapa Unificado (HU-04.6) ──────────────────────────

class PuntoMapaUnificadoSerializer(serializers.ModelSerializer):
    """
    Serializer optimizado para el mapa general.
    Solo retorna lo necesario para renderizar el marcador Leaflet.
    """
    ultimo_ica = serializers.SerializerMethodField()

    class Meta:
        model  = PuntoMonitoreo
        fields = [
            'id', 'nombre', 'tipo', 'latitud', 'longitud',
            'activo', 'ultimo_ica'
        ]

    def get_ultimo_ica(self, obj):
        if obj.tipo == 'AIRE' and hasattr(obj, 'estacion_aire'):
            ultima = obj.estacion_aire.muestras.first()
            if ultima:
                return {
                    'valor': str(ultima.ica_valor),
                    'nivel': ultima.ica_nivel,
                }
        return None