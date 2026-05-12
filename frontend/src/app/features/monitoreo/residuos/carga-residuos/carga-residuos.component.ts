import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MonitoreoService } from '../../monitoreo.service';

@Component({
  selector: 'app-carga-residuos',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './carga-residuos.component.html',
})
export class CargaResiduosComponent implements OnInit {

  puntos    = signal<any[]>([]);
  guardando = signal(false);
  exito     = signal(false);
  errorMsg  = signal('');

  form: any = {
    punto_residuos: '',
    fecha: '',
    tipo_residuo: 'MIXTO',
    peso_toneladas: '',
    operador: 'Operador Sak\'a Churu'
  };

  tipos = [
    { id: 'ORGANICO', nombre: 'Orgánico' },
    { id: 'RECICLABLE', nombre: 'Reciclable' },
    { id: 'ESPECIAL', nombre: 'Especial' },
    { id: 'MIXTO', nombre: 'Mixto (Común)' }
  ];

  constructor(private monitoreo: MonitoreoService) {}

  ngOnInit(): void {
    // Poner la fecha de hoy por defecto
    const hoy = new Date();
    this.form.fecha = hoy.toISOString().slice(0, 10);

    // Traer los puntos de residuos (Rellenos, Puntos Verdes)
    this.monitoreo.getMapaUnificado('RESIDUOS').subscribe({
      next: (data) => this.puntos.set(data.puntos),
      error: () => this.errorMsg.set('No se pudieron cargar los rellenos sanitarios.')
    });
  }

  onGuardar(): void {
    if (!this.form.punto_residuos || !this.form.peso_toneladas) {
      this.errorMsg.set('El punto y el peso son obligatorios.');
      return;
    }

    this.guardando.set(true);
    this.errorMsg.set('');
    this.exito.set(false);

    const payload = {
      punto_residuos: +this.form.punto_residuos,
      fecha: this.form.fecha,
      tipo_residuo: this.form.tipo_residuo,
      peso_toneladas: +this.form.peso_toneladas,
      operador: this.form.operador
    };

    this.monitoreo.registrarPesaje(payload).subscribe({
      next: () => {
        this.guardando.set(false);
        this.exito.set(true);
        this.form.peso_toneladas = ''; // Limpiar el peso para el siguiente camión
      },
      error: (err) => {
        this.guardando.set(false);
        this.errorMsg.set('Error al guardar el registro en la base de datos.');
      }
    });
  }
}