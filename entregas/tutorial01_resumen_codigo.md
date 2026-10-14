# Tutorial 01 - Resumen de código

## Service Layer

`CompraService` obtiene el libro y su inventario, valida las existencias, solicita
al `OrdenBuilder` la creación de la orden, delega el cobro al procesador inyectado y
actualiza el inventario. La lógica de negocio ya no reside en la vista.

Archivo: `tienda_app/services.py`.

## Vista

`CompraView` separa los verbos HTTP mediante `get()` y `post()`. Su responsabilidad
es crear el servicio con una dependencia proporcionada por `PaymentFactory`, pasar
el contexto a la plantilla y convertir los resultados o errores en respuestas web.

Archivo: `tienda_app/views.py`.

## Principios aplicados

- SRP: vista, servicio, cálculo de impuestos y gateway tienen responsabilidades
  independientes.
- OCP: se pueden incorporar nuevos procesadores sin reescribir el flujo de compra.
- DIP: el servicio recibe un procesador de pago, en vez de construir un banco
  concreto.
- Service Layer: la orquestación de la compra se encuentra en un único componente.

## Código de `services.py`

```python
from django.shortcuts import get_object_or_404

from .domain.builders import OrdenBuilder
from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro


class CompraService:
    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()

    def obtener_detalle_producto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {"libro": libro, "total": total}

    def ejecutar_compra(
        self, libro_id, cantidad=1, direccion="", usuario=None
    ):
        libro = get_object_or_404(Libro, id=libro_id)
        inventario = get_object_or_404(Inventario, libro=libro)

        if inventario.cantidad < cantidad:
            raise ValueError("No hay suficiente stock para completar la compra.")

        orden = (
            self.builder
            .con_usuario(usuario)
            .con_libro(libro)
            .con_cantidad(cantidad)
            .para_envio(direccion)
            .build()
        )

        if not self.procesador_pago.pagar(orden.total):
            orden.delete()
            raise Exception("La transacción fue rechazada por el banco.")

        inventario.cantidad -= cantidad
        inventario.save()
        return orden.total
```

## Código de `views.py`

```python
from django.shortcuts import render
from django.views import View

from .infra.factories import PaymentFactory
from .services import CompraService


class CompraView(View):
    template_name = "tienda_app/compra.html"

    def setup_service(self):
        gateway = PaymentFactory.get_processor()
        return CompraService(procesador_pago=gateway)

    def get(self, request, libro_id):
        contexto = self.setup_service().obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        servicio = self.setup_service()
        try:
            total = servicio.ejecutar_compra(libro_id, cantidad=1)
            return render(request, self.template_name, {
                "mensaje_exito": f"¡Gracias por su compra! Total: ${total}",
                "total": total,
            })
        except Exception as error:
            return render(
                request, self.template_name, {"error": str(error)}, status=400
            )
```
