import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { MonitoreoService } from '../../monitoreo.service';

@Component({
  selector: 'app-carga-datos-aire',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './carga-datos-aire.component.html',
})
export class CargaDatosAireComponent implements OnInit {

  estaciones   = signal<any[]>([]);
  guardando    = signal(false);
  exito        = signal(false);
  errorMsg     = signal('');
  resultadoICA = signal<any>(null);

  // Lista de parámetros trasladada aquí para que Angular no se confunda
  parametros = [
    {key:'pm25', label:'Material Particulado 2.5', short:'PM2.5', unit:'µg/m³'},
    {key:'pm10', label:'Material Particulado 10', short:'PM10', unit:'µg/m³'},
    {key:'no2', label:'Dióxido de Nitrógeno', short:'NO₂', unit:'µg/m³'},
    {key:'so2', label:'Dióxido de Azufre', short:'SO₂', unit:'µg/m³'},
    {key:'co', label:'Monóxido de Carbono', short:'CO', unit:'ppm'},
    {key:'o3', label:'Ozono Troposférico', short:'O₃', unit:'µg/m³'}
  ];

  // Volvemos a un "any" normal para evitar errores de sintaxis
  form: any = {
    estacion:  '',
    fecha_hora: '',
    pm25: '', pm10: '',
    no2:  '', so2:  '',
    co:   '', o3:   '',
  };

  constructor(private monitoreo: MonitoreoService) {}

  ngOnInit(): void {
    const ahora = new Date();
    ahora.setMinutes(ahora.getMinutes() - ahora.getTimezoneOffset());
    this.form.fecha_hora = ahora.toISOString().slice(0, 16);

    this.monitoreo.getEstacionesAire().subscribe({
      next: (data) => this.estaciones.set(data),
      error: () => this.errorMsg.set('No se pudieron cargar las estaciones de la Red MoniCA.')
    });
  }

  onGuardar(): void {
    if (!this.form.estacion || !this.form.fecha_hora) {
      this.errorMsg.set('La estación y la fecha son campos obligatorios.');
      setTimeout(() => this.errorMsg.set(''), 4000);
      return;
    }

    this.guardando.set(true);
    this.errorMsg.set('');
    this.exito.set(false);
    this.resultadoICA.set(null);

    const payload: any = {
      estacion:   +this.form.estacion,
      fecha_hora: this.form.fecha_hora,
    };

    this.parametros.forEach(p => {
      const v = this.form[p.key];
      if (v !== '' && v !== null) payload[p.key] = +v;
    });

    this.monitoreo.registrarMuestraAire(payload).subscribe({
      next: (resp) => {
        this.guardando.set(false);
        this.exito.set(true);
        this.resultadoICA.set({
          valor: resp.ica_valor,
          nivel: resp.ica_nivel,
          contaminante: resp.ica_contaminante_critico,
        });
        this.limpiarForm();
        setTimeout(() => this.exito.set(false), 8000);
      },
      error: (err) => {
        this.guardando.set(false);
        this.errorMsg.set(err?.error?.detail ?? 'Error al guardar la muestra. Verifique los datos.');
      }
    });
  }

  getNivelColor(nivel: string): string {
    const map: Record<string, string> = {
      BUENO:    'bg-emerald-100 text-emerald-800 border-emerald-400',
      MODERADO: 'bg-yellow-100 text-yellow-800 border-yellow-400',
      SENSIBLE: 'bg-orange-100 text-orange-800 border-orange-400',
      DANINO:   'bg-red-100 text-red-800 border-red-400',
      MUY_DAN:  'bg-purple-100 text-purple-800 border-purple-400',
    };
    return map[nivel] ?? 'bg-gray-100 text-gray-800 border-gray-300';
  }

  private limpiarForm(): void {
    const ahora = new Date();
    ahora.setMinutes(ahora.getMinutes() - ahora.getTimezoneOffset());
    this.form = {
      estacion: this.form.estacion,
      fecha_hora: ahora.toISOString().slice(0, 16),
      pm25: '', pm10: '', no2: '', so2: '', co: '', o3: '',
    };
  }
}