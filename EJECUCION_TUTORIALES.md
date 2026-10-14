# Ejecución de los tutoriales 01, 02 y 03

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

La creación real de `Servidor-Django` en AWS Academy, la apertura del puerto 8000
y la captura con la IP pública requieren que el laboratorio esté iniciado y exista
una sesión autenticada en AWS Academy. No había navegador ni sesión AWS disponible
durante esta ejecución.
