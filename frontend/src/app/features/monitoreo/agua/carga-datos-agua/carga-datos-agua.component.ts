import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MonitoreoService } from '../../monitoreo.service';

@Component({
  selector: 'app-carga-datos-agua',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './carga-datos-agua.component.html',
})
export class CargaDatosAguaComponent implements OnInit {

  puntos    = signal<any[]>([]);
  guardando = signal(false);
  exito     = signal(false);
  errorMsg  = signal('');
  resultado = signal<any>(null);

  parametros = [
    {key:'ph', label:'pH', unit:'0-14'},
    {key:'dbo', label:'DBO₅', unit:'mg/L'},
    {key:'dqo', label:'DQO', unit:'mg/L'},
    {key:'coliformes', label:'Coliformes', unit:'UFC/100ml'},
    {key:'turbidez', label:'Turbidez', unit:'NTU'},
    {key:'temperatura', label:'Temp.', unit:'°C'}
  ];

  form: any = {
    punto_agua: '',
    fecha_hora: '',
    ph: '', dbo: '', dqo: '',
    coliformes: '', turbidez: '', temperatura: '',
  };

  constructor(private monitoreo: MonitoreoService) {}

  ngOnInit(): void {
    const ahora = new Date();
    ahora.setMinutes(ahora.getMinutes() - ahora.getTimezoneOffset());
    this.form.fecha_hora = ahora.toISOString().slice(0, 16);

    this.monitoreo.getPuntosAgua().subscribe({
      next: (data) => this.puntos.set(data),
      error: () => this.errorMsg.set('No se pudieron cargar los puntos hídricos.')
    });
  }

  onGuardar(): void {
    if (!this.form.punto_agua || !this.form.fecha_hora) {
      this.errorMsg.set('Punto de muestreo y fecha son obligatorios.');
      setTimeout(() => this.errorMsg.set(''), 4000);
      return;
    }

    this.guardando.set(true);
    this.errorMsg.set('');
    this.exito.set(false);
    this.resultado.set(null);

    const payload: any = {
      punto_agua: +this.form.punto_agua,
      fecha_hora: this.form.fecha_hora,
    };

    this.parametros.forEach(p => {
      const v = this.form[p.key];
      if (v !== '' && v !== null) payload[p.key] = +v;
    });

    this.monitoreo.registrarMuestraAgua(payload).subscribe({
      next: (resp) => {
        this.guardando.set(false);
        this.exito.set(true);
        this.resultado.set({
          cumple: resp.cumple_ley,
          excedidos: resp.parametros_excedidos,
        });
        this.limpiarForm();
        setTimeout(() => this.exito.set(false), 8000);
      },
      error: (err) => {
        this.guardando.set(false);
        this.errorMsg.set(err?.error?.detail ?? 'Error al guardar el registro.');
      }
    });
  }

  private limpiarForm(): void {
    const ahora = new Date();
    ahora.setMinutes(ahora.getMinutes() - ahora.getTimezoneOffset());
    this.form = {
      punto_agua: this.form.punto_agua,
      fecha_hora: ahora.toISOString().slice(0, 16),
      ph: '', dbo: '', dqo: '',
      coliformes: '', turbidez: '', temperatura: '',
    };
  }
}