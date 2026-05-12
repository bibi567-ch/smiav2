from django.db import models
import random

class DenunciaAmbiental(models.Model):
    TIPOS_CHOICES = [
        ('Contaminación Aire', 'Contaminación del aire / Emisiones'),
        ('Contaminación Ríos', 'Contaminación de ríos'),
        ('Tala Ilegal', 'Tala ilegal de árboles'),
        ('Basura', 'Acumulación de basura / Residuos'),
        ('Ruido', 'Ruido excesivo comercial'),
        ('Otro', 'Otro problema ambiental'),
    ]

    tipo = models.CharField(max_length=100, choices=TIPOS_CHOICES)
    ubicacion = models.CharField(max_length=255)
    descripcion = models.TextField()
    email_contacto = models.EmailField(blank=True, null=True)

    numero_seguimiento = models.CharField(max_length=15, unique=True, editable=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='Pendiente') 

    def save(self, *args, **kwargs):
        if not self.numero_seguimiento:
            self.numero_seguimiento = f"SMGA-{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_seguimiento} - {self.tipo}"