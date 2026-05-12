// src/app/app.routes.ts
import { Routes } from '@angular/router';

export const routes: Routes = [
  // Portal ciudadano — página de inicio pública
  {
    path: '',
    loadComponent: () =>
      import('./components/portal-ciudadano/portal-ciudadano.component')
        .then(m => m.PortalCiudadanoComponent)
  },

  // Dashboard técnico — requiere login
  {
    path: 'dashboard',
    loadComponent: () =>
      import('./features/monitoreo/dashboard-tecnico/dashboard-tecnico.component')
        .then(m => m.DashboardTecnicoComponent)
  },

  // Módulos de monitoreo
  {
    path: 'monitoreo/aire',
    loadComponent: () =>
      import('./features/monitoreo/aire/mapa-aire/mapa-aire.component')
        .then(m => m.MapaAireComponent)
  },
  {
    path: 'monitoreo/aire/carga',
    loadComponent: () =>
      import('./features/monitoreo/aire/carga-datos-aire/carga-datos-aire.component')
        .then(m => m.CargaDatosAireComponent)
  },
  {
    path: 'monitoreo/agua',
    loadComponent: () =>
      import('./features/monitoreo/agua/mapa-agua/mapa-agua.component')
        .then(m => m.MapaAguaComponent)
  },
  {
    path: 'monitoreo/agua/carga',
    loadComponent: () =>
      import('./features/monitoreo/agua/carga-datos-agua/carga-datos-agua.component')
        .then(m => m.CargaDatosAguaComponent)
  },
  {
    path: 'monitoreo/ruido',
    loadComponent: () =>
      import('./features/monitoreo/ruido/carga-ruido/carga-ruido.component')
        .then(m => m.CargaRuidoComponent)
  },
  {
    path: 'monitoreo/vehicular',
    loadComponent: () =>
      import('./features/monitoreo/vehicular/carga-vehicular/carga-vehicular.component')
        .then(m => m.CargaVehicularComponent)
  },
  {
    path: 'monitoreo/residuos',
    loadComponent: () =>
      import('./features/monitoreo/residuos/carga-residuos/carga-residuos.component')
        .then(m => m.CargaResiduosComponent)
  },

  { path: '**', redirectTo: '' }
];