import {
  Component, Input, AfterViewInit,
  OnDestroy, ViewChild, ElementRef
} from '@angular/core';
import * as L from 'leaflet';

export interface PuntoMapa {
  id: number;
  nombre: string;
  tipo: string;
  latitud: number;
  longitud: number;
  activo: boolean;
  ultimo_ica?: { valor: string; nivel: string } | null;
}

@Component({
  selector:    'app-mapa-leaflet',
  standalone:  true,
  template: `
    <div #contenedor
         [style.height]="altura"
         class="w-full rounded-xl border border-gray-200 shadow-sm relative z-0">
    </div>
  `
})
export class MapaLeafletComponent implements AfterViewInit, OnDestroy {

  @ViewChild('contenedor') contenedor!: ElementRef;
  @Input() altura   = '400px';
  @Input() centroLat = -16.5000;
  @Input() centroLng = -68.1500;
  @Input() zoom      = 12;

  private mapa!: L.Map;
  private marcadores: L.Marker[] = [];

  private COLORES: Record<string, string> = {
    AIRE:      '#10b981',
    AGUA:      '#3b82f6',
    RESIDUOS:  '#f59e0b',
    RUIDO:     '#8b5cf6',
    VEHICULAR: '#ef4444',
  };

  private COLORES_ICA: Record<string, string> = {
    BUENO:    '#00e400',
    MODERADO: '#ffff00',
    SENSIBLE: '#ff7e00',
    DANINO:   '#ff0000',
    MUY_DAN:  '#8f3f97',
  };

  private EMOJIS: Record<string, string> = {
    AIRE: '💨', AGUA: '💧', RESIDUOS: '🗑️',
    RUIDO: '🔊', VEHICULAR: '🚗'
  };

  ngAfterViewInit(): void {
    // Esperamos un instante para asegurar que la pantalla existe antes de cargar el mapa
    setTimeout(() => this.inicializar(), 100);
  }

  ngOnDestroy(): void {
    if (this.mapa) {
      this.mapa.remove();
    }
  }

  private inicializar(): void {
    // Arreglamos los íconos AQUÍ adentro, para que no choquen al inicio
    const iconDefault = L.icon({
      iconUrl:       'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
      iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
      shadowUrl:     'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
      iconSize:    [25, 41],
      iconAnchor:  [12, 41],
      popupAnchor: [1, -34],
      shadowSize:  [41, 41]
    });
    L.Marker.prototype.options.icon = iconDefault;

    this.mapa = L.map(this.contenedor.nativeElement, {
      center: [this.centroLat, this.centroLng],
      zoom:   this.zoom,
    });
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap | SMIA GAMLP',
      maxZoom: 19,
    }).addTo(this.mapa);
  }

  renderizar(puntos: PuntoMapa[]): void {
    if (!this.mapa) return;
    
    this.marcadores.forEach(m => m.remove());
    this.marcadores = [];

    puntos.forEach(p => {
      const color = p.tipo === 'AIRE' && p.ultimo_ica
        ? (this.COLORES_ICA[p.ultimo_ica.nivel] ?? this.COLORES[p.tipo])
        : this.COLORES[p.tipo] ?? '#6b7280';

      const icono = L.divIcon({
        html: `<div style="background:${color};border:2px solid white;
                border-radius:50%;width:34px;height:34px;
                display:flex;align-items:center;justify-content:center;
                box-shadow:0 2px 6px rgba(0,0,0,.35);font-size:15px;">
                ${this.EMOJIS[p.tipo] ?? '📍'}
               </div>`,
        iconSize: [34, 34], iconAnchor: [17, 17], className: ''
      });

      const ica = p.ultimo_ica
        ? `<br><b>ICA:</b> ${p.ultimo_ica.valor} (${p.ultimo_ica.nivel})`
        : '';

      const m = L.marker([+p.latitud, +p.longitud], { icon: icono })
        .bindPopup(`<b>${p.nombre}</b><br>${p.tipo}${ica}`)
        .addTo(this.mapa);

      this.marcadores.push(m);
    });

    if (puntos.length > 0) {
      const grupo = L.featureGroup(this.marcadores);
      this.mapa.fitBounds(grupo.getBounds().pad(0.15));
    }
  }
}