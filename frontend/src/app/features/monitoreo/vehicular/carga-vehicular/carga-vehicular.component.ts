import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MonitoreoService } from '../../monitoreo.service';

@Component({
  selector: 'app-carga-vehicular',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './carga-vehicular.component.html',
})
export class CargaVehicularComponent implements OnInit {

  puntos    = signal<any[]>([]);
  guardando = signal(false);
  exito     = signal(false);
  errorMsg  = signal('');

  form: any = {
    punto: '',
    fecha_hora: '',
    placa: '',
    tipo_vehiculo: 'Minibus / Transporte Público',
    anio_vehiculo: '',
    co_pct: '',
    hc_ppm: '',
    nox_ppm: '',
    opacidad_pct: '',
    cumple_norma: true // true = Aprobado, false = Rechazado
  };

  tiposVehiculo = [
    'Minibus / Transporte Público',
    'Taxi / Trufi',
    'Vehículo Particular',
    'Motocicleta',
    'Transporte Pesado / Carga'
  ];

  constructor(private monitoreo: MonitoreoService) {}

  ngOnInit(): void {
    const ahora = new Date();
    ahora.setMinutes(ahora.getMinutes() - ahora.getTimezoneOffset());
    this.form.fecha_hora = ahora.toISOString().slice(0, 16);

    this.monitoreo.getMapaUnificado('VEHICULAR').subscribe({
      next: (data) => this.puntos.set(data.puntos),
      error: () => this.errorMsg.set('No se pudieron cargar los puntos de control vehicular.')
    });
  }

  onGuardar(): void {
    if (!this.form.punto || !this.form.placa) {
      this.errorMsg.set('El punto de control y la placa son obligatorios.');
      return;
    }

    this.guardando.set(true);
    this.errorMsg.set('');
    this.exito.set(false);

    const payload = { ...this.form, punto: +this.form.punto };

    // Limpiar campos vacíos para que no den error en la base de datos
    ['co_pct', 'hc_ppm', 'nox_ppm', 'opacidad_pct', 'anio_vehiculo'].forEach(k => {
      if (payload[k] === '') payload[k] = null;
      else payload[k] = +payload[k];
    });

    this.monitoreo.registrarMedicionVehicular(payload).subscribe({
      next: () => {
        this.guardando.set(false);
        this.exito.set(true);
        // Reiniciar datos del auto para el siguiente en la fila
        this.form.placa = '';
        this.form.co_pct = ''; this.form.hc_ppm = ''; 
        this.form.nox_ppm = ''; this.form.opacidad_pct = '';
      },
      error: () => {
        this.guardando.set(false);
        this.errorMsg.set('Error al registrar la roseta ambiental.');
      }
    });
  }
}