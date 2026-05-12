// mapa-aire.component.ts
import {
  Component, OnInit, signal,
  ViewChild, AfterViewInit
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { MonitoreoService } from '../../monitoreo.service';
import {
  MapaLeafletComponent, PuntoMapa
} from '../../../../shared/mapa-leaflet/mapa-leaflet.component';

@Component({
  selector:    'app-mapa-aire',
  standalone:  true,
  imports:     [CommonModule, RouterLink, MapaLeafletComponent],
  templateUrl: './mapa-aire.component.html',
})
export class MapaAireComponent implements OnInit, AfterViewInit {

  @ViewChild(MapaLeafletComponent) mapa!: MapaLeafletComponent;

  puntos      = signal<PuntoMapa[]>([]);
  cargando    = signal(true);
  totalPuntos = signal(0);
  puntoBueno  = signal(0);
  puntoModerado = signal(0);
  puntoCritico  = signal(0);

  constructor(private monitoreo: MonitoreoService) {}

  ngOnInit(): void {
    this.cargarPuntos();
  }

  ngAfterViewInit(): void {}

  cargarPuntos(): void {
    this.cargando.set(true);
    this.monitoreo.getMapaUnificado('AIRE').subscribe({
      next: (data) => {
        this.puntos.set(data.puntos);
        this.totalPuntos.set(data.total);

        // Contar por nivel
        let buenos = 0, moderados = 0, criticos = 0;
        data.puntos.forEach((p: any) => {
          if (!p.ultimo_ica) return;
          if (p.ultimo_ica.nivel === 'BUENO')    buenos++;
          else if (p.ultimo_ica.nivel === 'MODERADO') moderados++;
          else criticos++;
        });
        this.puntoBueno.set(buenos);
        this.puntoModerado.set(moderados);
        this.puntoCritico.set(criticos);

        this.cargando.set(false);

        // Renderizar mapa después de cargar datos
        setTimeout(() => {
          if (this.mapa) {
            this.mapa.renderizar(data.puntos);
          }
        }, 200);
      },
      error: () => this.cargando.set(false)
    });
  }
}