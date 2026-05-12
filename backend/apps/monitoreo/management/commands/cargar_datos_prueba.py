# apps/monitoreo/management/commands/cargar_datos_prueba.py
"""
Comando para cargar datos de prueba del SMIA.
Crea estaciones, puntos de monitoreo y muestras iniciales.
Uso: python manage.py cargar_datos_prueba
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import UsuarioSMIA
from apps.monitoreo.models import (
    PuntoMonitoreo, EstacionAire, PuntoAgua,
    PuntoResiduos, MedicionRuido, MedicionVehicular,
    MuestraAire, MuestraAgua, PesajeResiduos
)
from apps.monitoreo.calculadora_ica import calcular_ica
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Carga datos de prueba para el SMIA'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cargando datos de prueba...')

        # Obtener usuario admin
        try:
            admin = UsuarioSMIA.objects.filter(
                is_superuser=True
            ).first()
            if not admin:
                self.stdout.write(
                    self.style.ERROR('No hay superusuario. '
                        'Ejecuta primero: python manage.py createsuperuser')
                )
                return
        except Exception:
            self.stdout.write(
                self.style.ERROR('Error al obtener superusuario.')
            )
            return

        # ── Estaciones de Aire (Red MoniCA) ──────────────────────────
        estaciones_data = [
            {
                'nombre': 'Estación Centro Histórico',
                'lat': -16.4955, 'lng': -68.1336,
                'codigo': 'MON-001', 'tipo': 'AUTOMATICA'
            },
            {
                'nombre': 'Estación Zona Sur — Calacoto',
                'lat': -16.5420, 'lng': -68.0890,
                'codigo': 'MON-002', 'tipo': 'AUTOMATICA'
            },
            {
                'nombre': 'Estación Villa Fátima',
                'lat': -16.4780, 'lng': -68.1100,
                'codigo': 'MON-003', 'tipo': 'ACTIVA'
            },
            {
                'nombre': 'Estación Miraflores',
                'lat': -16.4890, 'lng': -68.1020,
                'codigo': 'MON-004', 'tipo': 'AUTOMATICA'
            },
            {
                'nombre': 'Estación Sopocachi',
                'lat': -16.5100, 'lng': -68.1200,
                'codigo': 'MON-005', 'tipo': 'PASIVA'
            },
            {
                'nombre': 'Estación El Alto — Ciudad Satélite',
                'lat': -16.5100, 'lng': -68.1900,
                'codigo': 'MON-006', 'tipo': 'AUTOMATICA'
            },
        ]

        for data in estaciones_data:
            punto, creado = PuntoMonitoreo.objects.get_or_create(
                nombre=data['nombre'],
                defaults={
                    'tipo':       'AIRE',
                    'latitud':    data['lat'],
                    'longitud':   data['lng'],
                    'activo':     True,
                    'creado_por': admin,
                }
            )
            EstacionAire.objects.get_or_create(
                codigo_monica=data['codigo'],
                defaults={
                    'punto':         punto,
                    'tipo_estacion': data['tipo'],
                }
            )
            if creado:
                self.stdout.write(f'  ✓ Estación: {data["nombre"]}')

        # ── Puntos de Agua ────────────────────────────────────────────
        puntos_agua_data = [
            {
                'nombre': 'Río Choqueyapu — Puente Topater',
                'lat': -16.4980, 'lng': -68.1410,
                'tipo': 'RIO', 'cuenca': 'Cuenca Choqueyapu'
            },
            {
                'nombre': 'Río Irpavi — Sector Cota Cota',
                'lat': -16.5380, 'lng': -68.0950,
                'tipo': 'RIO', 'cuenca': 'Cuenca Irpavi'
            },
            {
                'nombre': 'Laguna Milluni — Zona Norte',
                'lat': -16.3800, 'lng': -68.1600,
                'tipo': 'LAGUNA', 'cuenca': 'Cuenca Altiplano'
            },
            {
                'nombre': 'Río Orkojahuira — Sector Miraflores',
                'lat': -16.4820, 'lng': -68.0980,
                'tipo': 'RIO', 'cuenca': 'Cuenca Orkojahuira'
            },
        ]

        for data in puntos_agua_data:
            punto, creado = PuntoMonitoreo.objects.get_or_create(
                nombre=data['nombre'],
                defaults={
                    'tipo':       'AGUA',
                    'latitud':    data['lat'],
                    'longitud':   data['lng'],
                    'activo':     True,
                    'creado_por': admin,
                }
            )
            PuntoAgua.objects.get_or_create(
                punto=punto,
                defaults={
                    'tipo_cuerpo': data['tipo'],
                    'cuenca':      data['cuenca'],
                }
            )
            if creado:
                self.stdout.write(f'  ✓ Punto agua: {data["nombre"]}')

        # ── Puntos de Residuos ────────────────────────────────────────
        puntos_residuos_data = [
            {
                'nombre': "Relleno Sanitario Sak'a Churu",
                'lat': -16.6200, 'lng': -68.2100,
                'tipo_punto': 'RELLENO',
                'capacidad': 850.0,
                'operador': 'EMAVERDE'
            },
            {
                'nombre': 'Punto Verde — Plaza Avaroa',
                'lat': -16.5050, 'lng': -68.1230,
                'tipo_punto': 'P_VERDE',
                'capacidad': 5.0,
                'operador': 'GAMLP'
            },
            {
                'nombre': 'Punto Verde — Sopocachi',
                'lat': -16.5120, 'lng': -68.1180,
                'tipo_punto': 'P_VERDE',
                'capacidad': 5.0,
                'operador': 'GAMLP'
            },
        ]

        for data in puntos_residuos_data:
            punto, creado = PuntoMonitoreo.objects.get_or_create(
                nombre=data['nombre'],
                defaults={
                    'tipo':       'RESIDUOS',
                    'latitud':    data['lat'],
                    'longitud':   data['lng'],
                    'activo':     True,
                    'creado_por': admin,
                }
            )
            PuntoResiduos.objects.get_or_create(
                punto=punto,
                defaults={
                    'tipo_punto':    data['tipo_punto'],
                    'capacidad_ton': data['capacidad'],
                    'operador':      data['operador'],
                }
            )
            if creado:
                self.stdout.write(f'  ✓ Punto residuos: {data["nombre"]}')

        # ── Puntos de Ruido ───────────────────────────────────────────
        puntos_ruido_data = [
            {
                'nombre': 'Control Acústico — Av. Arce',
                'lat': -16.5030, 'lng': -68.1180
            },
            {
                'nombre': 'Control Acústico — Zona Norte',
                'lat': -16.4780, 'lng': -68.1320
            },
            {
                'nombre': 'Control Acústico — El Alto',
                'lat': -16.5080, 'lng': -68.1950
            },
        ]

        for data in puntos_ruido_data:
            PuntoMonitoreo.objects.get_or_create(
                nombre=data['nombre'],
                defaults={
                    'tipo':       'RUIDO',
                    'latitud':    data['lat'],
                    'longitud':   data['lng'],
                    'activo':     True,
                    'creado_por': admin,
                }
            )
            self.stdout.write(f'  ✓ Punto ruido: {data["nombre"]}')

        # ── Puntos Vehiculares ────────────────────────────────────────
        puntos_veh_data = [
            {
                'nombre': 'Operativo Vehicular — Av. Montes',
                'lat': -16.4920, 'lng': -68.1350
            },
            {
                'nombre': 'Operativo Vehicular — El Alto',
                'lat': -16.5020, 'lng': -68.1880
            },
            {
                'nombre': 'Operativo Vehicular — Miraflores',
                'lat': -16.4870, 'lng': -68.1050
            },
        ]

        for data in puntos_veh_data:
            PuntoMonitoreo.objects.get_or_create(
                nombre=data['nombre'],
                defaults={
                    'tipo':       'VEHICULAR',
                    'latitud':    data['lat'],
                    'longitud':   data['lng'],
                    'activo':     True,
                    'creado_por': admin,
                }
            )
            self.stdout.write(f'  ✓ Punto vehicular: {data["nombre"]}')

        # ── Muestras de Aire históricas ───────────────────────────────
        self.stdout.write('\nGenerando muestras de aire históricas...')
        estaciones = EstacionAire.objects.all()

        for estacion in estaciones:
            # 7 días de datos, cada 6 horas
            for dias in range(7):
                for hora in [0, 6, 12, 18]:
                    fecha = timezone.now() - timedelta(days=dias, hours=hora)
                    pm25 = round(random.uniform(8, 45), 4)
                    pm10 = round(random.uniform(15, 70), 4)
                    no2  = round(random.uniform(20, 90), 4)

                    resultado = calcular_ica(
                        pm25=pm25, pm10=pm10, no2=no2
                    )

                    MuestraAire.objects.get_or_create(
                        estacion=estacion,
                        fecha_hora=fecha,
                        defaults={
                            'pm25':                     pm25,
                            'pm10':                     pm10,
                            'no2':                      no2,
                            'ica_valor':                resultado.valor,
                            'ica_nivel':                resultado.nivel,
                            'ica_contaminante_critico': resultado.contaminante_critico,
                            'registrado_por':           admin,
                        }
                    )

        self.stdout.write('\n' + self.style.SUCCESS(
            '✅ Datos de prueba cargados correctamente.\n'
            f'   - {EstacionAire.objects.count()} estaciones de aire\n'
            f'   - {PuntoAgua.objects.count()} puntos de agua\n'
            f'   - {PuntoResiduos.objects.count()} puntos de residuos\n'
            f'   - {PuntoMonitoreo.objects.filter(tipo="RUIDO").count()} puntos de ruido\n'
            f'   - {PuntoMonitoreo.objects.filter(tipo="VEHICULAR").count()} puntos vehiculares\n'
            f'   - {MuestraAire.objects.count()} muestras de aire\n'
        ))