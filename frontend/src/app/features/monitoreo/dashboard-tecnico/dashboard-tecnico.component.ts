// dashboard-tecnico.component.ts
import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../../services/auth.service';
import { MonitoreoService } from '../monitoreo.service';

@Component({
  selector:    'app-dashboard-tecnico',
  standalone:  true,
  imports:     [CommonModule, RouterLink],
  templateUrl: './dashboard-tecnico.component.html',
})
export class DashboardTecnicoComponent implements OnInit {

  usuario    = this.auth.usuarioActual;
  cargando   = signal(true);
  totalPuntos = signal(0);

  modulos = [
    { titulo: 'Calidad del Aire',   ruta: '/monitoreo/aire',
      icono: '💨', color: 'emerald',
      desc: 'Red MoniCA — ICA automático EPA' },
    { titulo: 'Calidad del Agua',   ruta: '/monitoreo/agua',
      icono: '💧', color: 'blue',
      desc: 'Parámetros vs Ley N°1333' },
    { titulo: 'Residuos',           ruta: '/monitoreo/residuos',
      icono: '🗑️', color: 'amber',
      desc: 'Pesaje Sak\'a Churu — SIGIR' },
    { titulo: 'Ruido',              ruta: '/monitoreo/ruido',
      icono: '🔊', color: 'purple',
      desc: 'Control acústico — REGAM' },
    { titulo: 'Emisiones Vehiculares', ruta: '/monitoreo/vehicular',
      icono: '🚗', color: 'red',
      desc: 'Operativos — PTDI 2021-2025' },
  ];

  constructor(
    public  auth:       AuthService,
    private monitoreo:  MonitoreoService
  ) {}

  ngOnInit(): void {
    this.monitoreo.getMapaUnificado().subscribe({
      next: (data) => {
        this.totalPuntos.set(data.total);
        this.cargando.set(false);
      },
      error: () => this.cargando.set(false)
    });
  }

  logout(): void {
    this.auth.logout();
  }
}