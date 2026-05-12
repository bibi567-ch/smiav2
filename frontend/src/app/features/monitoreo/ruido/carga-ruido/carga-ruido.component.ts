import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MonitoreoService } from '../../monitoreo.service';

@Component({
  selector: 'app-carga-ruido',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './carga-ruido.component.html',
})
export class CargaRuidoComponent implements OnInit {

  puntos    = signal<any[]>([]);
  guardando = signal(false);
  exito     = signal(false);
  errorMsg  = signal('');
  resultado = signal<any>(null);

  form = {
    punto: '',
    fecha_hora: '',
    zona: 'RESIDENCIAL',
    nivel_db: '',
    es_nocturno: false,
    observaciones: ''
  };

  zonas = [
    { id: 'RESIDENCIAL', nombre: 'Residencial (Límite: 55dB Día / 45dB Noche)' },
    { id: 'COMERCIAL',   nombre: 'Comercial (Límite: 65dB Día / 55dB Noche)' },
    { id: 'INDUSTRIAL',  nombre: 'Industrial (Límite: 75dB Día / 65dB Noche)' }
  ];

  constructor(private monitoreo: MonitoreoService) {}

  ngOnInit(): void {
    const ahora = new Date();
    ahora.setMinutes(ahora.getMinutes() - ahora.getTimezoneOffset());
    this.form.fecha_hora = ahora.toISOString().slice(0, 16);

    this.monitoreo.getMapaUnificado('RUIDO').subscribe({
      next: (data) => this.puntos.set(data.puntos),
      error: () => this.errorMsg.set('No se pudieron cargar los puntos de monitoreo de ruido.')
    });
  }

  onGuardar(): void {
    if (!this.form.punto || !this.form.nivel_db) {
      this.errorMsg.set('El punto y el nivel de decibeles (dB) son obligatorios.');
      return;
    }

    this.guardando.set(true);
    this.errorMsg.set('');
    this.exito.set(false);
    this.resultado.set(null);

    const payload = {
      punto: +this.form.punto,
      fecha_hora: this.form.fecha_hora,
      zona: this.form.zona,
      nivel_db: +this.form.nivel_db,
      es_nocturno: this.form.es_nocturno,
      observaciones: this.form.observaciones
    };

    this.monitoreo.registrarMedicionRuido(payload).subscribe({
      next: (resp) => {
        this.guardando.set(false);
        this.exito.set(true);
        this.resultado.set({
          excedencia: resp.es_excedencia,
          nivel: resp.nivel_db
        });
        this.form.nivel_db = '';
        this.form.observaciones = '';
      },
      error: (err) => {
        this.guardando.set(false);
        this.errorMsg.set('Error al registrar la medición acústica.');
      }
    });
  }
}