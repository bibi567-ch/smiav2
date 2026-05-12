// features/monitoreo/monitoreo.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '../../services/auth.service';

@Injectable({ providedIn: 'root' })
export class MonitoreoService {

  private readonly API = '/api/monitoreo';

  constructor(
    private http: HttpClient,
    private auth: AuthService
  ) {}

  // ── Mapa unificado (público) ─────────────────────────────────────
  getMapaUnificado(tipo?: string): Observable<any> {
    const params = tipo ? `?tipo=${tipo}` : '';
    return this.http.get(`${this.API}/mapa/${params}`);
  }

  // ── Estaciones de Aire ───────────────────────────────────────────
  getEstacionesAire(): Observable<any> {
    return this.http.get(
      `${this.API}/aire/estaciones/`,
      { headers: this.auth.headers() }
    );
  }

  crearEstacionAire(data: any): Observable<any> {
    return this.http.post(
      `${this.API}/aire/estaciones/`,
      data,
      { headers: this.auth.headers() }
    );
  }

  // ── Muestras de Aire ─────────────────────────────────────────────
  getMuestrasAire(estacionId?: number): Observable<any> {
    const params = estacionId ? `?estacion=${estacionId}` : '';
    return this.http.get(
      `${this.API}/aire/muestras/${params}`,
      { headers: this.auth.headers() }
    );
  }

  registrarMuestraAire(data: any): Observable<any> {
    return this.http.post(
      `${this.API}/aire/muestras/`,
      data,
      { headers: this.auth.headers() }
    );
  }

  subirCSVAire(formData: FormData): Observable<any> {
    return this.http.post(
      `${this.API}/aire/carga-csv/`,
      formData,
      { headers: this.auth.headers() }
    );
  }

  // ── Agua ─────────────────────────────────────────────────────────
  getPuntosAgua(): Observable<any> {
    return this.http.get(
      `${this.API}/agua/puntos/`,
      { headers: this.auth.headers() }
    );
  }

  registrarMuestraAgua(data: any): Observable<any> {
    return this.http.post(
      `${this.API}/agua/muestras/`,
      data,
      { headers: this.auth.headers() }
    );
  }

  getMuestrasAgua(puntoId?: number): Observable<any> {
    const params = puntoId ? `?punto=${puntoId}` : '';
    return this.http.get(
      `${this.API}/agua/muestras/${params}`,
      { headers: this.auth.headers() }
    );
  }

  // ── Ruido ────────────────────────────────────────────────────────
  registrarMedicionRuido(data: any): Observable<any> {
    return this.http.post(
      `${this.API}/ruido/mediciones/`,
      data,
      { headers: this.auth.headers() }
    );
  }

  getMedicionesRuido(): Observable<any> {
    return this.http.get(
      `${this.API}/ruido/mediciones/`,
      { headers: this.auth.headers() }
    );
  }

  // ── Residuos ─────────────────────────────────────────────────────
  registrarPesaje(data: any): Observable<any> {
    return this.http.post(
      `${this.API}/residuos/pesajes/`,
      data,
      { headers: this.auth.headers() }
    );
  }

  getPesajes(): Observable<any> {
    return this.http.get(
      `${this.API}/residuos/pesajes/`,
      { headers: this.auth.headers() }
    );
  }

  // ── Vehicular ────────────────────────────────────────────────────
  registrarMedicionVehicular(data: any): Observable<any> {
    return this.http.post(
      `${this.API}/vehicular/mediciones/`,
      data,
      { headers: this.auth.headers() }
    );
  }
}