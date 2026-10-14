# 1. Usamos una imagen base oficial de Python ligera.
FROM python:3.11-slim

# 2. Evitamos archivos .pyc y usamos salida sin buffer para los logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor.
WORKDIR /app

# 4. Instalamos las dependencias antes de copiar el código para aprovechar la caché.
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el código fuente.
COPY . /app/

# 6. Puerto y comando por defecto del servidor de desarrollo del laboratorio.
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
