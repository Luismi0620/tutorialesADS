import datetime
from pathlib import Path

from django.conf import settings

from ..domain.interfaces import ProcesadorPago

class BancoNacionalProcesador(ProcesadorPago):
    """
    Implementación concreta de la infraestructura.
    Simula un banco local escribiendo en un log.
    """
    def __init__(self, tutorial_numero=1):
        self.tutorial_numero = int(tutorial_numero)

    def pagar(self, monto: float, contexto=None) -> bool:
        nombre_log = f"pagos_tutorial{self.tutorial_numero:02d}_MIRAL.log"
        archivo_log = Path(settings.BASE_DIR) / nombre_log
        detalle_inventario = ""
        if contexto:
            detalle_inventario = (
                f" | Libro: {contexto['libro_id']} - {contexto['titulo']}"
                f" | Inventario: {contexto['inventario_anterior']}"
                f" -> {contexto['inventario_nuevo']}"
            )

        with archivo_log.open("a", encoding="utf-8") as f:
            f.write(
                f"[{datetime.datetime.now()}] "
                f"Transaccion exitosa por: ${monto}"
                f"{detalle_inventario}\n"
            )
        return True
