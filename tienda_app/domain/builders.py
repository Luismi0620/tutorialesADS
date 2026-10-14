from decimal import Decimal

from ..models import Orden
from .logic import CalculadorImpuestos


class OrdenBuilder:
    """Construye una orden paso a paso mediante una interfaz fluida."""

    def __init__(self):
        self.reset()

    def reset(self):
        self._usuario = None
        self._libro = None
        self._cantidad = 1
        self._direccion = ""

    def con_usuario(self, usuario):
        self._usuario = usuario
        return self

    def con_libro(self, libro):
        self._libro = libro
        return self

    def con_cantidad(self, cantidad):
        if cantidad < 1:
            raise ValueError("La cantidad debe ser mayor que cero.")
        self._cantidad = cantidad
        return self

    def para_envio(self, direccion):
        self._direccion = direccion
        return self

    def build(self) -> Orden:
        if self._libro is None:
            raise ValueError("Datos insuficientes para crear la orden.")

        total_unitario = Decimal(
            str(CalculadorImpuestos.obtener_total_con_iva(self._libro.precio))
        )
        total = total_unitario * self._cantidad

        orden = Orden.objects.create(
            usuario=self._usuario,
            libro=self._libro,
            total=total,
            direccion_envio=self._direccion,
        )
        self.reset()
        return orden
