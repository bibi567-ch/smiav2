# backend/Dockerfile
FROM python:3.12-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalamos dependencias del sistema necesarias para PostGIS y psycopg2
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiamos e instalamos las dependencias de Python
# Nota: Asegúrate de tener un archivo requirements.txt en tu carpeta backend
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Comando para iniciar el servidor de desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]