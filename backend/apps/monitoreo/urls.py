# apps/monitoreo/urls.py
from django.urls import path
from .views import (
    MapaUnificadoView,
    EstacionAireListCreateView, EstacionAireDetailView,
    MuestraAireListCreateView, CargaCSVAireView,
    PuntoAguaListCreateView, MuestraAguaListCreateView,
    PesajeResiduosListCreateView,
    MedicionRuidoListCreateView,
    MedicionVehicularListCreateView,
)

urlpatterns = [
    # Mapa unificado — público
    path('mapa/',                    MapaUnificadoView.as_view()),

    # Aire
    path('aire/estaciones/',         EstacionAireListCreateView.as_view()),
    path('aire/estaciones/<int:pk>/',EstacionAireDetailView.as_view()),
    path('aire/muestras/',           MuestraAireListCreateView.as_view()),
    path('aire/carga-csv/',          CargaCSVAireView.as_view()),

    # Agua
    path('agua/puntos/',             PuntoAguaListCreateView.as_view()),
    path('agua/muestras/',           MuestraAguaListCreateView.as_view()),

    # Residuos
    path('residuos/pesajes/',        PesajeResiduosListCreateView.as_view()),

    # Ruido
    path('ruido/mediciones/',        MedicionRuidoListCreateView.as_view()),

    # Vehicular
    path('vehicular/mediciones/',    MedicionVehicularListCreateView.as_view()),
]