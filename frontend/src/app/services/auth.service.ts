// src/app/services/auth.service.ts
import { Injectable, signal } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap, catchError, throwError } from 'rxjs';

export interface Usuario {
  id: number;
  email: string;
  nombres: string;
  apellidos: string;
  nombre_completo: string;
  rol: string;
}

interface RespuestaLogin {
  access: string;
  refresh: string;
  usuario: Usuario;
}

@Injectable({ providedIn: 'root' })
export class AuthService {

  readonly usuarioActual = signal<Usuario | null>(null);
  readonly cargando      = signal<boolean>(false);

  private readonly API       = '/api';
  private readonly TOKEN_KEY = 'smia_access';
  private readonly REF_KEY   = 'smia_refresh';
  private apiUrl = 'http://127.0.0.1:8000/api/auth';

  constructor(
    private http:   HttpClient,
    private router: Router
  ) {
    this.restaurarSesion();
  }

  login(email: string, password: string): Observable<RespuestaLogin> {
    this.cargando.set(true);
    return this.http.post<RespuestaLogin>(
      `${this.apiUrl}/login/`,
      { email, password }
    ).pipe(
      tap(resp => {
        localStorage.setItem(this.TOKEN_KEY, resp.access);
        localStorage.setItem(this.REF_KEY,   resp.refresh);
        this.usuarioActual.set(resp.usuario);
        this.cargando.set(false);
        this.redirigir(resp.usuario.rol);
      }),
      catchError(err => {
        this.cargando.set(false);
        return throwError(() => err);
      })
    );
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.REF_KEY);
    this.usuarioActual.set(null);
    this.router.navigate(['/']);
  }

  obtenerToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  estaAutenticado(): boolean {
    return !!this.obtenerToken();
  }

  headers(): HttpHeaders {
    return new HttpHeaders({
      Authorization: `Bearer ${this.obtenerToken()}`
    });
  }

  private restaurarSesion(): void {
    const token = this.obtenerToken();
    if (!token) return;
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      if (payload.exp * 1000 > Date.now()) {
        this.http.get<Usuario>(`${this.API}/auth/perfil/`, {
          headers: this.headers()
        }).subscribe({
          next:  u  => this.usuarioActual.set(u),
          error: () => this.logout()
        });
      } else {
        this.logout();
      }
    } catch {
      this.logout();
    }
  }

  private redirigir(rol: string): void {
    const rutas: Record<string, string> = {
      ADMIN:         '/dashboard',
      DIRECTOR:      '/dashboard',
      TECNICO_AIRE:  '/monitoreo/aire',
      TECNICO_AGUA:  '/monitoreo/agua',
      TECNICO_RES:   '/monitoreo/residuos',
      TECNICO_RUIDO: '/monitoreo/ruido',
      TECNICO_VEH:   '/monitoreo/vehicular',
      AUDITOR:       '/dashboard',
      CIUDADANO:     '/',
    };
    this.router.navigate([rutas[rol] ?? '/dashboard']);
  }
}