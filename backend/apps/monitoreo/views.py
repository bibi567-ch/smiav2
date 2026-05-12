# apps/monitoreo/views.py
"""
Endpoints REST del módulo de monitoreo.
Cumple: RF-04, RF-05, RF-08, RF-10
"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
import csv
import io

from .models import (
    PuntoMonitoreo, EstacionAire, MuestraAire,
    PuntoAgua, MuestraAgua,
    PuntoResiduos, PesajeResiduos,
    MedicionRuido, MedicionVehicular
)
from .serializers import (
    EstacionAireSerializer, EstacionAireCreateSerializer,
    MuestraAireSerializer,
    PuntoAguaSerializer, PuntoAguaCreateSerializer,
    MuestraAguaSerializer,
    PesajeResiduosSerializer,
    MedicionRuidoSerializer,
    MedicionVehicularSerializer,
    PuntoMapaUnificadoSerializer,
)
from .calculadora_ica import calcular_ica


# ── MAPA UNIFICADO — HU-04.6, RF-10 ─────────────────────────────────

class MapaUnificadoView(APIView):
    """
    GET /api/monitoreo/mapa/
    Retorna todos los puntos activos para el mapa Leaflet.
    Acceso público — HU-08.1
    """
    permission_classes = [AllowAny]

    def get(self, request):
        tipo  = request.query_params.get('tipo', None)
        puntos = PuntoMonitoreo.objects.filter(activo=True)

        if tipo:
            puntos = puntos.filter(tipo=tipo.upper())

        serializer = PuntoMapaUnificadoSerializer(puntos, many=True)
        return Response({
            'total': puntos.count(),
            'puntos': serializer.data,
        })


# ── ESTACIONES DE AIRE — HU-04.1 ────────────────────────────────────

class EstacionAireListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/monitoreo/aire/estaciones/  — Lista estaciones
    POST /api/monitoreo/aire/estaciones/  — Crea estación
    """
    queryset = EstacionAire.objects.select_related('punto').all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EstacionAireCreateSerializer
        return EstacionAireSerializer


class EstacionAireDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/monitoreo/aire/estaciones/<id>/"""
    queryset           = EstacionAire.objects.all()
    serializer_class   = EstacionAireSerializer


# ── MUESTRAS DE AIRE — HU-05.1 ──────────────────────────────────────

class MuestraAireListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/monitoreo/aire/muestras/  — Lista muestras
    POST /api/monitoreo/aire/muestras/  — Registra muestra (ICA auto)
    """
    serializer_class = MuestraAireSerializer

    def get_queryset(self):
        qs = MuestraAire.objects.select_related(
            'estacion__punto'
        ).all()
        estacion_id = self.request.query_params.get('estacion')
        if estacion_id:
            qs = qs.filter(estacion_id=estacion_id)
        return qs


class CargaCSVAireView(APIView):
    """
    POST /api/monitoreo/aire/carga-csv/
    Carga masiva de datos desde archivo CSV de la Red MoniCA.
    Cumple: HU-05.1 (manejo de errores por fila)
    """
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        archivo = request.FILES.get('archivo')
        if not archivo:
            return Response(
                {'error': 'No se adjuntó ningún archivo.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        estacion_id = request.data.get('estacion_id')
        if not estacion_id:
            return Response(
                {'error': 'Se requiere el ID de la estación.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            estacion = EstacionAire.objects.get(id=estacion_id)
        except EstacionAire.DoesNotExist:
            return Response(
                {'error': 'Estación no encontrada.'},
                status=status.HTTP_404_NOT_FOUND
            )

        contenido   = archivo.read().decode('utf-8')
        reader      = csv.DictReader(io.StringIO(contenido))
        guardados   = 0
        errores     = []

        for num_fila, fila in enumerate(reader, start=2):
            try:
                data = {
                    'estacion':  estacion.id,
                    'fecha_hora': fila.get('fecha_hora', '').strip(),
                    'pm25': fila.get('pm25') or None,
                    'pm10': fila.get('pm10') or None,
                    'no2':  fila.get('no2')  or None,
                    'so2':  fila.get('so2')  or None,
                    'co':   fila.get('co')   or None,
                    'o3':   fila.get('o3')   or None,
                }
                serializer = MuestraAireSerializer(
                    data=data,
                    context={'request': request}
                )
                if serializer.is_valid():
                    serializer.save()
                    guardados += 1
                else:
                    errores.append({
                        'fila': num_fila,
                        'errores': serializer.errors
                    })
            except Exception as e:
                errores.append({'fila': num_fila, 'error': str(e)})

        return Response({
            'guardados': guardados,
            'errores':   errores,
            'mensaje': f'{guardados} registros procesados correctamente.'
        })


# ── PUNTOS DE AGUA — HU-04.2 ────────────────────────────────────────

class PuntoAguaListCreateView(generics.ListCreateAPIView):
    queryset = PuntoAgua.objects.select_related('punto').all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PuntoAguaCreateSerializer
        return PuntoAguaSerializer


class MuestraAguaListCreateView(generics.ListCreateAPIView):
    """ICA de agua calculado automáticamente vs Ley N°1333."""
    serializer_class = MuestraAguaSerializer

    def get_queryset(self):
        qs = MuestraAgua.objects.select_related('punto_agua__punto').all()
        punto_id = self.request.query_params.get('punto')
        if punto_id:
            qs = qs.filter(punto_agua_id=punto_id)
        return qs


# ── PESAJE RESIDUOS — HU-05.3 ───────────────────────────────────────

class PesajeResiduosListCreateView(generics.ListCreateAPIView):
    serializer_class = PesajeResiduosSerializer

    def get_queryset(self):
        return PesajeResiduos.objects.select_related(
            'punto_residuos__punto'
        ).all()


# ── MEDICIONES RUIDO — HU-04.4 / HU-05.4 ───────────────────────────

class MedicionRuidoListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicionRuidoSerializer

    def get_queryset(self):
        qs = MedicionRuido.objects.select_related('punto').all()
        zona = self.request.query_params.get('zona')
        if zona:
            qs = qs.filter(zona=zona.upper())
        return qs


# ── MEDICIONES VEHICULARES — HU-04.5 / HU-05.5 ──────────────────────

class MedicionVehicularListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicionVehicularSerializer

    def get_queryset(self):
        return MedicionVehicular.objects.select_related('punto').all()