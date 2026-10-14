# Tutorial 03 - Evidencia DRF y API

## Solicitud

```http
POST /api/v1/comprar/ HTTP/1.1
Content-Type: application/json

{
  "libro_id": 2,
  "direccion_envio": "Calle Evidencia Inventario",
  "cantidad": 1
}
```

## Respuesta

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "estado": "exito",
  "mensaje": "Orden creada. Total: 178.5"
}
```

## Consistencia entre API y HTML

Antes de la solicitud, `Clean Code en Python` tenía 7 unidades. El endpoint REST
reutilizó `CompraService`, creó la orden y dejó 6 unidades. Después de la compra,
`GET /compra/2/` respondió 200 y mostró `Stock disponible: 6`, demostrando que la
vista HTML y la API comparten la misma lógica y base de datos.

## Log independiente

La Factory creó un `BancoNacionalProcesador` configurado para el tutorial 3. Las
transacciones quedaron registradas exclusivamente en `pagos_tutorial03_MIRAL.log`;
los tres registros anteriores permanecen en `pagos_tutorial01_MIRAL.log`.

```text
[2026-10-14 11:57:03.265057] Transaccion exitosa por: $178.5 | Libro: 2 - Clean Code en Python | Inventario: 7 -> 6
[2026-10-14 11:58:36.296294] Transaccion exitosa por: $214.2 | Libro: 4 - Patrones de Diseno | Inventario: 8 -> 7
```

## Captura

`captura_tutorial03_drf.png` muestra la interfaz navegable de Django REST
Framework después de enviar un POST: `HTTP 201 Created` y el mensaje
`Orden creada. Total: 214.2`.

`captura_tutorial03_inventario_html.png` muestra la otra puerta de entrada: la
vista HTML de `Clean Code en Python` con `Stock disponible: 6` después del POST
realizado por API.
