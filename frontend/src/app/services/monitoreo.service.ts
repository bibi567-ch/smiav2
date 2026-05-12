import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class MonitoreoService {

  // La dirección de tu backend en Django
  private readonly API = 'http://127.0.0.1:8000/api/monitoreo';

  constructor(private http: HttpClient) {}

  // Busca la llave de seguridad (Token) del usuario que inició sesión
  private headers(): HttpHeaders {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({ Authorization: `Bearer ${token}` });
  }

  // ── Mapa unificado (Público) ─────────────────────────────────────
  getPuntosMapaUnificado(tipo?: string): Observable<any> {
    const params = tipo ? `?tipo=${tipo}` : '';
    return this.http.get(`${this.API}/mapa/${params}`);
  }

  // ── Aire ─────────────────────────────────────────────────────────
  getEstacionesAire(): Observable<any> {
    return this.http.get(`${this.API}/aire/estaciones/`, { headers: this.headers() });
  }

  crearEstacionAire(data: any): Observable<any> {
    return this.http.post(`${this.API}/aire/estaciones/`, data, { headers: this.headers() });
  }

  getMuestrasAire(estacionId?: number): Observable<any> {
    const params = estacionId ? `?estacion=${estacionId}` : '';
    return this.http.get(`${this.API}/aire/muestras/${params}`, { headers: this.headers() });
  }

  registrarMuestraAire(data: any): Observable<any> {
    return this.http.post(`${this.API}/aire/muestras/`, data, { headers: this.headers() });
  }

  // ── Agua ─────────────────────────────────────────────────────────
  getPuntosAgua(): Observable<any> {
    return this.http.get(`${this.API}/agua/puntos/`, { headers: this.headers() });
  }

  registrarMuestraAgua(data: any): Observable<any> {
    return this.http.post(`${this.API}/agua/muestras/`, data, { headers: this.headers() });
  }

  // ── Residuos ─────────────────────────────────────────────────────
  registrarPesaje(data: any): Observable<any> {
    return this.http.post(`${this.API}/residuos/pesajes/`, data, { headers: this.headers() });
  }
}