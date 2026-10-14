# Ejecución de los tutoriales 01 al 06

Este proyecto se clonó en una carpeta nueva y se trabajó en la rama
`tutoriales-completados`, partiendo del primer commit del repositorio para evitar las
implementaciones de tutoriales posteriores que ya estaban incorporadas en `master`.

## Tutorial 01 - Django, SOLID y Service Layer

1. Se clonó `https://github.com/Nram94/TEIS-DjangoSOLID`.
2. Se creó `venv` y se instaló Django 6.1.2.
3. Se ejecutaron las migraciones sobre SQLite.
4. Se crearon tres libros con inventario: `Clean Code en Python`,
   `Arquitectura Limpia` y `Patrones de Diseno`.
5. La vista basada en clases separa `GET` y `POST` y delega la compra en
   `CompraService`.
6. `CompraService` concentra la validación de stock, el cálculo, el pago y la
   persistencia.
7. `BancoNacionalProcesador` genera `pagos_tutorial01_MIRAL.log` en la raíz del
   proyecto.
8. Se ejecutaron tres compras de libros diferentes y se comprobaron tres líneas
   en el log.

## Tutorial 02 - Factory Method y Builder

1. Se creó `tienda_app/infra/factories.py` con `PaymentFactory` y
   `MockPaymentProcessor`.
2. La variable `PAYMENT_PROVIDER=MOCK` selecciona el procesador simulado; sin la
   variable se utiliza el banco.
3. Se creó `tienda_app/domain/builders.py` con una interfaz fluida para usuario,
   libro, cantidad y dirección de envío.
4. Se ampliaron `Orden` y su migración con usuario y dirección de envío.
5. `CompraService` usa el Builder y recibe el procesador seleccionado por la
   Factory.
6. Se ejecutó una compra en modo MOCK y se obtuvo el mensaje de depuración
   esperado.

## Verificación reproducible

```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py test -v 2

$env:PAYMENT_PROVIDER = "MOCK"
.\venv\Scripts\python.exe manage.py runserver
```

La adaptación respecto al pseudocódigo del PDF es intencional: el modelo original
relaciona cada `Orden` con un solo `Libro`, por lo que el Builder usa `con_libro()`
y `con_cantidad()` en vez de intentar guardar una lista en un campo inexistente.

## Tutorial 03 - API REST con DRF

1. Se instalaron Django REST Framework, Markdown y django-filter.
2. Se registraron `rest_framework` y `django_filters` en `INSTALLED_APPS`.
3. Se creó `LibroSerializer`, que expone el stock calculado, y
   `OrdenInputSerializer`, que valida el DTO de compra.
4. Se creó `CompraAPIView`, que reutiliza `CompraService` y selecciona el gateway
   mediante `PaymentFactory`.
5. Se publicó `POST /api/v1/comprar/`.
6. Las compras reales por API devolvieron `201 Created`. El inventario de
   `Clean Code en Python` cambió de 7 a 6 y el de `Patrones de Diseno`, de 8 a 7.
7. Cada línea de `pagos_tutorial03_MIRAL.log` contiene el pago, el libro y los
   valores anterior y nuevo del inventario.
8. Un `GET /compra/2/` posterior mostró `Stock disponible: 6` en la vista HTML.
9. Se guardó `entregas/captura_tutorial03_drf.png`, que muestra la interfaz DRF,
   el estado 201 y la respuesta JSON de una compra.
10. `entregas/captura_tutorial03_inventario_html.png` muestra el stock 6 desde la
    puerta HTML después de comprar por la puerta API.

Los logs quedan separados por tutorial:

- `pagos_tutorial01_MIRAL.log`: tres compras del tutorial 1.
- `pagos_tutorial03_MIRAL.log`: compras REST del tutorial 3.

## Tutorial 04 - Docker y AWS

1. `settings.py` usa PostgreSQL y lee `DB_NAME`, `DB_USER`, `DB_PASSWORD`,
   `DB_HOST` y `DB_PORT` del entorno.
2. `requirements.txt` fue congelado e incluye `psycopg2-binary` y DRF.
3. Se creó el `Dockerfile` basado en `python:3.11-slim`.
4. Se creó `docker-compose.yml` con Django, PostgreSQL 15 y volumen persistente.
5. La imagen fue construida correctamente y ambos contenedores quedaron activos;
   PostgreSQL reportó estado saludable.
6. Las migraciones se aplicaron automáticamente dentro del contenedor.
7. Dos solicitudes reales devolvieron `201 Created` y total `142.80`; el
   inventario persistido cambió `5 -> 4 -> 3`.
8. Las transacciones se aislaron en `pagos_tutorial04_MIRAL.log`.
9. `captura_tutorial04_docker_local.png` muestra la respuesta de la API servida
   desde Docker.
10. Se prepararon `scripts/aws_ec2_setup.sh` y `scripts/aws_ec2_deploy.sh` para
    ejecutar los comandos indicados por el tutorial en Amazon Linux 2023.
11. Se desplegó la aplicación en una instancia Amazon Linux 2023 de AWS Academy.
12. La API pública respondió `201 Created` desde el puerto 8000 y la evidencia se
    guardó en `entregas/captura_tutorial04_aws.png`.

## Tutorial 05 - Nginx, Gunicorn y Strangler Pattern

1. Se agregó Gunicorn a `requirements.txt` y al comando predeterminado de la
   imagen Docker.
2. Se creó `nginx/nginx.conf` con el upstream interno `web:8000`.
3. Django dejó de publicar el puerto 8000 hacia el host y ahora se ejecuta con
   `gunicorn Tienda.wsgi:application`.
4. Se añadió el servicio `nginx`, que es el único que publica un puerto hacia el
   host (`80:80`).
5. `TUTORIAL_NUMERO=5` separa las nuevas transacciones en
   `pagos_tutorial05_MIRAL.log`.
6. La configuración se validó localmente con tres contenedores activos: `db`,
   `web` y `nginx`.
7. Las 10 pruebas automatizadas pasaron dentro del contenedor de Django.
8. `http://localhost/api/v1/comprar/` respondió a través de Nginx y el acceso
   directo a `http://localhost:8000/` fue rechazado.

Las tres capturas de AWS requeridas por el tutorial 5 se documentan en
`entregas/tutorial05_evidencia.md`.

## Tutorial 06 - Primer estrangulamiento con Flask

1. Se creó `microservicio_pagos/app.py` con el endpoint independiente
   `POST /api/v2/comprar`.
2. El microservicio se dockerizó con Python Alpine y Gunicorn.
3. Django conserva la API v1 y ahora expone `GET /api/v1/productos/` para la
   prueba de coexistencia requerida.
4. Docker Compose orquesta cuatro servicios: `db`, `web_django`,
   `pagos_flask` y `nginx`.
5. Nginx dirige `/api/v1/` al monolito Django en el puerto interno 8000 y
   `/api/v2/comprar` al microservicio Flask en el puerto interno 5000.
6. El formato de acceso de Nginx registra `upstream` y `upstream_status` para
   demostrar qué backend atendió cada solicitud.
7. Pasaron 11 pruebas de Django y 2 pruebas del microservicio Flask.
8. La prueba local obtuvo `200 OK` tanto para la lista v1 como para la compra
   v2; los logs mostraron upstreams diferentes (`:8000` y `:5000`).

Las evidencias requeridas para AWS se detallan en
`entregas/tutorial06_evidencia.md`.
