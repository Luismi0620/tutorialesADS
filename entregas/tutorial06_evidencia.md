# Tutorial 06 - Evidencias del primer estrangulamiento

## Arquitectura implementada

- `GET /api/v1/productos/` se atiende en Django/Gunicorn.
- `POST /api/v2/comprar` se atiende en Flask/Gunicorn.
- Nginx es la única puerta pública y decide el backend según la versión de API.
- PostgreSQL continúa disponible para el monolito Django.

## Verificación local

- 11 pruebas Django: correctas.
- 2 pruebas Flask: correctas.
- Respuesta v1: `200 OK` desde el upstream interno `:8000`.
- Respuesta v2: `200 OK` desde el upstream interno `:5000`.

## Evidencias pendientes en AWS Academy

1. `captura_tutorial06_django_v1.png`: Postman ejecutando
   `GET http://<IP-AWS>/api/v1/productos/` y mostrando la respuesta de Django.
2. `captura_tutorial06_flask_v2.png`: Postman ejecutando
   `POST http://<IP-AWS>/api/v2/comprar` con el cuerpo:

   ```json
   {
     "producto_id": 1,
     "cantidad": 2
   }
   ```

   La respuesta debe indicar que la compra fue procesada por el microservicio
   Flask v2.
3. `captura_tutorial06_logs_nginx.png`: terminal EC2 mostrando:

   ```bash
   docker compose logs --tail=30 nginx
   ```

   Deben observarse una solicitud v1 con upstream `:8000` y una solicitud v2
   con upstream `:5000`.

## Despliegue en EC2

```bash
cd ~/tutorialesADS
git pull origin main
docker compose up -d --build --remove-orphans
docker compose restart nginx
docker compose ps
```
