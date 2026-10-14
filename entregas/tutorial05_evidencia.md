# Tutorial 05 - Evidencias de Nginx, Gunicorn y aislamiento

## Verificación local completada

- Contenedores activos: PostgreSQL, Django/Gunicorn y Nginx.
- Nginx publica `0.0.0.0:80->80/tcp`.
- Django muestra únicamente `8000/tcp`, sin enlace al puerto del host.
- La API respondió mediante `http://localhost/api/v1/comprar/`.
- La conexión directa a `http://localhost:8000/` fue rechazada.
- Las 10 pruebas automatizadas terminaron correctamente.

## Evidencias pendientes en AWS Academy

1. `captura_tutorial05_nginx_aws.png`: navegador consumiendo
   `http://<IP-EC2>/api/v1/comprar/`, sin `:8000` en la URL.
2. `captura_tutorial05_puerto8000_bloqueado.png`: intento fallido de acceso a
   `http://<IP-EC2>:8000/`.
3. `captura_tutorial05_docker_ps_aws.png`: terminal EC2 con `docker ps` mostrando
   `nginx`, `web` y `db` en estado `Up`.

## Despliegue en EC2

```bash
cd ~/tutorialesADS
git pull origin main
docker compose up -d --build
docker ps
```

En el Security Group debe existir una regla HTTP para el puerto 80. Después de
validar el aislamiento, debe eliminarse la regla anterior del puerto 8000.
