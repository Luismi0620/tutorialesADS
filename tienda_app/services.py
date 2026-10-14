from django.shortcuts import get_object_or_404
from django.db import transaction

from .domain.builders import OrdenBuilder
from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro


class CompraService:
    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago
        self.builder = OrdenBuilder()

    def obtener_detalle_producto(self, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        inventario = get_object_or_404(Inventario, libro=libro)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {
            "libro": libro,
            "total": total,
            "stock": inventario.cantidad,
        }

    @transaction.atomic
    def ejecutar_compra(self, libro_id, cantidad=1, direccion="", usuario=None):
        libro = get_object_or_404(Libro, id=libro_id)
        inventario = get_object_or_404(
            Inventario.objects.select_for_update(),
            libro=libro,
        )

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

        inventario_anterior = inventario.cantidad
        inventario.cantidad -= cantidad
        inventario.save(update_fields=["cantidad"])

        contexto_pago = {
            "libro_id": libro.id,
            "titulo": libro.titulo,
            "inventario_anterior": inventario_anterior,
            "inventario_nuevo": inventario.cantidad,
        }
        if not self.procesador_pago.pagar(orden.total, contexto=contexto_pago):
            raise Exception("La transacción fue rechazada por el banco.")

        return orden.total
