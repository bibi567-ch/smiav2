// src/app/components/login/login.component.ts
import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <!-- Este componente ya no se usa directamente -->
    <!-- El login ahora es el modal dentro del portal ciudadano -->
    <p>Redirigiendo...</p>
  `
})
export class LoginComponent {
  constructor(private authService: AuthService) {}
}