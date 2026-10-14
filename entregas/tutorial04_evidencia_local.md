# Tutorial 04 - Dockerización y evidencia local

## Configuración

- Django obtiene `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT` del
  entorno.
- La configuración predeterminada utiliza PostgreSQL. Para ejecutar pruebas
  locales aisladas puede utilizarse `DB_ENGINE=sqlite`.
- `requirements.txt` incluye Django REST Framework y `psycopg2-binary`.

## Imagen Docker

El `Dockerfile` usa `python:3.11-slim`, desactiva `.pyc`, habilita la salida sin
buffer, instala dependencias y publica Django en `0.0.0.0:8000`.

## Orquestación

`docker-compose.yml` levanta:

- `db`: PostgreSQL 15 con el volumen persistente `postgres_data`.
- `web`: la aplicación Django, que espera la salud de PostgreSQL, ejecuta las
  migraciones y publica el puerto `8000`.
- `TUTORIAL_NUMERO=4` mantiene cualquier evidencia de pagos Docker/AWS separada
  en `pagos_tutorial04_MIRAL.log`.

Comando requerido:

```powershell
docker compose up --build
```

Endpoint de comprobación:

```text
http://localhost:8000/api/v1/comprar/
```

## Resultado verificado

- PostgreSQL 15: saludable.
- Django 5.2.8: iniciado en `0.0.0.0:8000`.
- Migraciones: aplicadas sin cambios pendientes.
- Solicitud `POST /api/v1/comprar/`: `201 Created`.
- Respuesta: `Orden creada. Total: 142.80`.
- Inventario de `Docker y AWS`: `5 -> 4` en la verificación programática y
  `4 -> 3` al generar la captura de la interfaz DRF.
- Log independiente: `pagos_tutorial04_MIRAL.log`.
- Captura: `entregas/captura_tutorial04_docker_local.png`, con `HTTP 201 Created`
  y `Orden creada. Total: 142.80`.

## Preparación de AWS

Se incluyen dos scripts equivalentes a los comandos del tutorial:

- `scripts/aws_ec2_setup.sh`: actualiza Amazon Linux, instala Git y Docker,
  inicia Docker y agrega `ec2-user` al grupo `docker`.
- `scripts/aws_ec2_deploy.sh`: clona una URL de repositorio, ejecuta
  `docker compose up -d --build` y muestra `docker ps`.

La ejecución real en EC2 requiere una sesión autenticada y un laboratorio activo
de AWS Academy, además de una URL que contenga estos cambios del proyecto.
