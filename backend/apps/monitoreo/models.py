# apps/monitoreo/models.py
"""
Modelos de monitoreo ambiental del SMIA.
Cubre: RF-04, RF-05 | HU-04.1 al HU-04.6 | HU-05.1 al HU-05.6
GAMLP — Secretaría Municipal de Gestión Ambiental
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import UsuarioSMIA


# ═══════════════════════════════════════════════════════════════════
# TIPOS Y CONSTANTES
# ═══════════════════════════════════════════════════════════════════

class TipoMonitoreo(models.TextChoices):
    AIRE      = 'AIRE',      'Calidad del Aire'
    AGUA      = 'AGUA',      'Calidad del Agua'
    RESIDUOS  = 'RESIDUOS',  'Gestión de Residuos'
    RUIDO     = 'RUIDO',     'Contaminación Acústica'
    VEHICULAR = 'VEHICULAR', 'Emisiones Vehiculares'


class TipoEstacionAire(models.TextChoices):
    PASIVA     = 'PASIVA',     'Estación Pasiva'
    AUTOMATICA = 'AUTOMATICA', 'Estación Automática'
    ACTIVA     = 'ACTIVA',     'Estación Activa'


class TipoCuerpoHidrico(models.TextChoices):
    RIO    = 'RIO',    'Río'
    LAGUNA = 'LAGUNA', 'Laguna'
    CANAL  = 'CANAL',  'Canal'


class TipoZonaRuido(models.TextChoices):
    RESIDENCIAL = 'RESIDENCIAL', 'Residencial'
    COMERCIAL   = 'COMERCIAL',   'Comercial'
    INDUSTRIAL  = 'INDUSTRIAL',  'Industrial'


class NivelICA(models.TextChoices):
    BUENO              = 'BUENO',    'Bueno (0-50)'
    MODERADO           = 'MODERADO', 'Moderado (51-100)'
    GRUPOS_SENSIBLES   = 'SENSIBLE', 'Dañino grupos sensibles (101-150)'
    DANINO             = 'DANINO',   'Dañino (151-200)'
    MUY_DANINO         = 'MUY_DAN',  'Muy dañino (201+)'


# ═══════════════════════════════════════════════════════════════════
# PUNTO DE MONITOREO — Base para todos los tipos (RF-04)
# ═══════════════════════════════════════════════════════════════════

class PuntoMonitoreo(models.Model):
    """
    Modelo base para todos los puntos georreferenciados del SMIA.
    Almacena coordenadas como latitud/longitud (sin PostGIS en SQLite).
    En producción con PostgreSQL/PostGIS se migra a PointField.
    Cumple: RF-04, HU-04.1 al HU-04.6
    """
    nombre          = models.CharField(max_length=200)
    tipo            = models.CharField(
                        max_length=20,
                        choices=TipoMonitoreo.choices
                      )
    latitud         = models.DecimalField(
                        max_digits=10, decimal_places=7,
                        help_text='Latitud WGS84. Ej: -16.5000'
                      )
    longitud        = models.DecimalField(
                        max_digits=10, decimal_places=7,
                        help_text='Longitud WGS84. Ej: -68.1500'
                      )
    descripcion     = models.TextField(blank=True)
    activo          = models.BooleanField(default=True)
    fecha_creacion  = models.DateTimeField(auto_now_add=True)
    creado_por      = models.ForeignKey(
                        UsuarioSMIA,
                        on_delete=models.SET_NULL,
                        null=True,
                        related_name='puntos_creados'
                      )

    class Meta:
        db_table  = 'smia_puntos_monitoreo'
        ordering  = ['-fecha_creacion']
        verbose_name        = 'Punto de Monitoreo'
        verbose_name_plural = 'Puntos de Monitoreo'

    def __str__(self):
        return f'{self.nombre} ({self.get_tipo_display()})'


# ═══════════════════════════════════════════════════════════════════
# ESTACIÓN DE AIRE — Red MoniCA (HU-04.1)
# ═══════════════════════════════════════════════════════════════════

class EstacionAire(models.Model):
    """
    Estaciones de la Red MoniCA del GAMLP.
    Cumple: HU-04.1, RF-04
    """
    punto           = models.OneToOneField(
                        PuntoMonitoreo,
                        on_delete=models.CASCADE,
                        related_name='estacion_aire'
                      )
    tipo_estacion   = models.CharField(
                        max_length=20,
                        choices=TipoEstacionAire.choices,
                        default=TipoEstacionAire.AUTOMATICA
                      )
    codigo_monica   = models.CharField(
                        max_length=20,
                        unique=True,
                        help_text='Código oficial Red MoniCA'
                      )

    class Meta:
        db_table            = 'smia_estaciones_aire'
        verbose_name        = 'Estación de Aire'
        verbose_name_plural = 'Estaciones de Aire'

    def __str__(self):
        return f'{self.codigo_monica} — {self.punto.nombre}'


# ═══════════════════════════════════════════════════════════════════
# MUESTRA DE AIRE — Datos ICA (HU-05.1)
# ═══════════════════════════════════════════════════════════════════

class MuestraAire(models.Model):
    """
    Registro de contaminantes atmosféricos.
    El ICA se calcula automáticamente al guardar — metodología EPA.
    Cumple: HU-05.1, RF-05
    """
    estacion        = models.ForeignKey(
                        EstacionAire,
                        on_delete=models.CASCADE,
                        related_name='muestras'
                      )
    fecha_hora      = models.DateTimeField()
    registrado_por  = models.ForeignKey(
                        UsuarioSMIA,
                        on_delete=models.SET_NULL,
                        null=True
                      )

    # Contaminantes (µg/m³ o ppm según parámetro)
    pm25            = models.DecimalField(
                        max_digits=8, decimal_places=4,
                        null=True, blank=True,
                        verbose_name='PM2.5 (µg/m³)'
                      )
    pm10            = models.DecimalField(
                        max_digits=8, decimal_places=4,
                        null=True, blank=True,
                        verbose_name='PM10 (µg/m³)'
                      )
    no2             = models.DecimalField(
                        max_digits=8, decimal_places=4,
                        null=True, blank=True,
                        verbose_name='NO₂ (µg/m³)'
                      )
    so2             = models.DecimalField(
                        max_digits=8, decimal_places=4,
                        null=True, blank=True,
                        verbose_name='SO₂ (µg/m³)'
                      )
    co              = models.DecimalField(
                        max_digits=8, decimal_places=4,
                        null=True, blank=True,
                        verbose_name='CO (ppm)'
                      )
    o3              = models.DecimalField(
                        max_digits=8, decimal_places=4,
                        null=True, blank=True,
                        verbose_name='O₃ (µg/m³)'
                      )

    # ICA calculado automáticamente
    ica_valor       = models.DecimalField(
                        max_digits=8, decimal_places=4,
                        null=True, blank=True,
                        verbose_name='ICA (4 decimales)'
                      )
    ica_nivel       = models.CharField(
                        max_length=10,
                        choices=NivelICA.choices,
                        blank=True
                      )
    ica_contaminante_critico = models.CharField(
                        max_length=10,
                        blank=True,
                        help_text='Contaminante que determinó el ICA'
                      )

    class Meta:
        db_table  = 'smia_muestras_aire'
        ordering  = ['-fecha_hora']
        verbose_name        = 'Muestra de Aire'
        verbose_name_plural = 'Muestras de Aire'

    def __str__(self):
        return f'{self.estacion} | ICA {self.ica_valor} | {self.fecha_hora}'


# ═══════════════════════════════════════════════════════════════════
# PUNTO DE AGUA (HU-04.2)
# ═══════════════════════════════════════════════════════════════════

class PuntoAgua(models.Model):
    """
    Sitio de muestreo hídrico — ríos, lagunas, canales.
    Cumple: HU-04.2, RF-04
    """
    punto           = models.OneToOneField(
                        PuntoMonitoreo,
                        on_delete=models.CASCADE,
                        related_name='punto_agua'
                      )
    tipo_cuerpo     = models.CharField(
                        max_length=20,
                        choices=TipoCuerpoHidrico.choices
                      )
    cuenca          = models.CharField(
                        max_length=100,
                        help_text='Ej: Cuenca del Río Choqueyapu'
                      )

    class Meta:
        db_table            = 'smia_puntos_agua'
        verbose_name        = 'Punto de Agua'
        verbose_name_plural = 'Puntos de Agua'

    def __str__(self):
        return f'{self.punto.nombre} ({self.get_tipo_cuerpo_display()})'


# ═══════════════════════════════════════════════════════════════════
# MUESTRA DE AGUA — Parámetros vs Ley N°1333 (HU-05.2)
# ═══════════════════════════════════════════════════════════════════

class MuestraAgua(models.Model):
    """
    Análisis físico-químico de calidad del agua.
    Se compara automáticamente contra límites de la Ley N°1333.
    Cumple: HU-05.2, RF-05
    """
    punto_agua      = models.ForeignKey(
                        PuntoAgua,
                        on_delete=models.CASCADE,
                        related_name='muestras'
                      )
    fecha_hora      = models.DateTimeField()
    registrado_por  = models.ForeignKey(
                        UsuarioSMIA,
                        on_delete=models.SET_NULL,
                        null=True
                      )

    # Parámetros físico-químicos
    ph              = models.DecimalField(
                        max_digits=5, decimal_places=2,
                        null=True, blank=True,
                        validators=[MinValueValidator(0), MaxValueValidator(14)],
                        verbose_name='pH'
                      )
    dbo             = models.DecimalField(
                        max_digits=8, decimal_places=2,
                        null=True, blank=True,
                        verbose_name='DBO₅ (mg/L)'
                      )
    dqo             = models.DecimalField(
                        max_digits=8, decimal_places=2,
                        null=True, blank=True,
                        verbose_name='DQO (mg/L)'
                      )
    coliformes      = models.DecimalField(
                        max_digits=12, decimal_places=2,
                        null=True, blank=True,
                        verbose_name='Coliformes fecales (UFC/100ml)'
                      )
    turbidez        = models.DecimalField(
                        max_digits=8, decimal_places=2,
                        null=True, blank=True,
                        verbose_name='Turbidez (NTU)'
                      )
    temperatura     = models.DecimalField(
                        max_digits=5, decimal_places=2,
                        null=True, blank=True,
                        verbose_name='Temperatura (°C)'
                      )

    # Resultado automático vs Ley N°1333
    cumple_ley      = models.BooleanField(
                        null=True,
                        verbose_name='Cumple Ley N°1333'
                      )
    parametros_excedidos = models.JSONField(
                        default=list,
                        verbose_name='Parámetros que exceden límites'
                      )

    class Meta:
        db_table  = 'smia_muestras_agua'
        ordering  = ['-fecha_hora']
        verbose_name        = 'Muestra de Agua'
        verbose_name_plural = 'Muestras de Agua'

    def __str__(self):
        cumple = '✓' if self.cumple_ley else '✗'
        return f'{self.punto_agua} | {cumple} Ley 1333 | {self.fecha_hora}'


# ═══════════════════════════════════════════════════════════════════
# PUNTO DE RESIDUOS (HU-04.3)
# ═══════════════════════════════════════════════════════════════════

class PuntoResiduos(models.Model):
    """
    Rellenos sanitarios, puntos verdes y rutas de recolección.
    Cumple: HU-04.3, RF-04
    """
    class TipoPunto(models.TextChoices):
        RELLENO      = 'RELLENO',   'Relleno Sanitario'
        PUNTO_VERDE  = 'P_VERDE',   'Punto Verde'
        TRANSFERENCIA = 'TRANSFER', 'Estación de Transferencia'

    punto           = models.OneToOneField(
                        PuntoMonitoreo,
                        on_delete=models.CASCADE,
                        related_name='punto_residuos'
                      )
    tipo_punto      = models.CharField(
                        max_length=20,
                        choices=TipoPunto.choices
                      )
    capacidad_ton   = models.DecimalField(
                        max_digits=10, decimal_places=2,
                        null=True, blank=True,
                        verbose_name='Capacidad (toneladas/día)'
                      )
    operador        = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table            = 'smia_puntos_residuos'
        verbose_name        = 'Punto de Residuos'
        verbose_name_plural = 'Puntos de Residuos'

    def __str__(self):
        return f'{self.punto.nombre} ({self.get_tipo_punto_display()})'


# ═══════════════════════════════════════════════════════════════════
# PESAJE DE RESIDUOS — Sak'a Churu (HU-05.3)
# ═══════════════════════════════════════════════════════════════════

class PesajeResiduos(models.Model):
    """
    Registro diario de pesaje en el relleno sanitario.
    Se sincroniza con SIGIR (Ley N°755).
    Cumple: HU-05.3, RF-05, RF-09
    """
    class TipoResiduo(models.TextChoices):
        ORGANICO    = 'ORGANICO',   'Orgánico'
        RECICLABLE  = 'RECICLABLE', 'Reciclable'
        ESPECIAL    = 'ESPECIAL',   'Especial'
        MIXTO       = 'MIXTO',      'Mixto'

    class EstadoSIGIR(models.TextChoices):
        PENDIENTE    = 'PENDIENTE',   'Pendiente de envío'
        SINCRONIZADO = 'SINCRONIZADO','Sincronizado con SIGIR'
        ERROR        = 'ERROR',       'Error de sincronización'

    punto_residuos  = models.ForeignKey(
                        PuntoResiduos,
                        on_delete=models.CASCADE,
                        related_name='pesajes'
                      )
    fecha           = models.DateField()
    tipo_residuo    = models.CharField(
                        max_length=20,
                        choices=TipoResiduo.choices
                      )
    peso_toneladas  = models.DecimalField(
                        max_digits=10, decimal_places=3,
                        verbose_name='Peso (toneladas)'
                      )
    operador        = models.CharField(max_length=200)
    registrado_por  = models.ForeignKey(
                        UsuarioSMIA,
                        on_delete=models.SET_NULL,
                        null=True
                      )
    sigir_estado    = models.CharField(
                        max_length=20,
                        choices=EstadoSIGIR.choices,
                        default=EstadoSIGIR.PENDIENTE
                      )
    sigir_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table  = 'smia_pesajes_residuos'
        ordering  = ['-fecha']
        verbose_name        = 'Pesaje de Residuos'
        verbose_name_plural = 'Pesajes de Residuos'

    def __str__(self):
        return f'{self.fecha} | {self.tipo_residuo} | {self.peso_toneladas} ton'


# ═══════════════════════════════════════════════════════════════════
# MEDICIÓN DE RUIDO (HU-04.4 / HU-05.4)
# ═══════════════════════════════════════════════════════════════════

class MedicionRuido(models.Model):
    """
    Medición acústica georreferenciada en dB.
    Alerta automática si supera el límite de la zona.
    Cumple: HU-04.4, HU-05.4, RF-04, RF-05
    """
    # Límites REGAM por zona (dB)
    LIMITES_ZONA = {
        'RESIDENCIAL': {'diurno': 55, 'nocturno': 45},
        'COMERCIAL':   {'diurno': 65, 'nocturno': 55},
        'INDUSTRIAL':  {'diurno': 75, 'nocturno': 65},
    }

    punto           = models.ForeignKey(
                        PuntoMonitoreo,
                        on_delete=models.CASCADE,
                        related_name='mediciones_ruido'
                      )
    fecha_hora      = models.DateTimeField()
    zona            = models.CharField(
                        max_length=20,
                        choices=TipoZonaRuido.choices
                      )
    nivel_db        = models.DecimalField(
                        max_digits=6, decimal_places=2,
                        verbose_name='Nivel de ruido (dB)'
                      )
    es_nocturno     = models.BooleanField(
                        default=False,
                        help_text='True si la medición es horario nocturno'
                      )
    es_excedencia   = models.BooleanField(
                        default=False,
                        verbose_name='Excede límite reglamentario'
                      )
    registrado_por  = models.ForeignKey(
                        UsuarioSMIA,
                        on_delete=models.SET_NULL,
                        null=True
                      )
    observaciones   = models.TextField(blank=True)

    class Meta:
        db_table  = 'smia_mediciones_ruido'
        ordering  = ['-fecha_hora']
        verbose_name        = 'Medición de Ruido'
        verbose_name_plural = 'Mediciones de Ruido'

    def __str__(self):
        excedencia = '⚠️' if self.es_excedencia else '✓'
        return f'{excedencia} {self.nivel_db} dB | {self.zona} | {self.fecha_hora}'


# ═══════════════════════════════════════════════════════════════════
# MEDICIÓN VEHICULAR (HU-04.5 / HU-05.5)
# ═══════════════════════════════════════════════════════════════════

class MedicionVehicular(models.Model):
    """
    Medición de gases en operativos vehiculares.
    Cumple: HU-04.5, HU-05.5, RF-04, RF-05
    """
    punto           = models.ForeignKey(
                        PuntoMonitoreo,
                        on_delete=models.CASCADE,
                        related_name='mediciones_vehiculares'
                      )
    fecha_hora      = models.DateTimeField()
    placa           = models.CharField(max_length=10)
    tipo_vehiculo   = models.CharField(max_length=50)
    anio_vehiculo   = models.PositiveSmallIntegerField(
                        null=True, blank=True,
                        verbose_name='Año del vehículo'
                      )

    # Gases medidos
    co_pct          = models.DecimalField(
                        max_digits=6, decimal_places=3,
                        null=True, blank=True,
                        verbose_name='CO (%)'
                      )
    hc_ppm          = models.DecimalField(
                        max_digits=8, decimal_places=2,
                        null=True, blank=True,
                        verbose_name='HC (ppm)'
                      )
    nox_ppm         = models.DecimalField(
                        max_digits=8, decimal_places=2,
                        null=True, blank=True,
                        verbose_name='NOx (ppm)'
                      )
    opacidad_pct    = models.DecimalField(
                        max_digits=5, decimal_places=2,
                        null=True, blank=True,
                        verbose_name='Opacidad (%)'
                      )

    cumple_norma    = models.BooleanField(verbose_name='Cumple norma')
    registrado_por  = models.ForeignKey(
                        UsuarioSMIA,
                        on_delete=models.SET_NULL,
                        null=True
                      )

    class Meta:
        db_table  = 'smia_mediciones_vehiculares'
        ordering  = ['-fecha_hora']
        verbose_name        = 'Medición Vehicular'
        verbose_name_plural = 'Mediciones Vehiculares'

    def __str__(self):
        estado = 'APTO' if self.cumple_norma else 'NO APTO'
        return f'{self.placa} | {estado} | {self.fecha_hora}'