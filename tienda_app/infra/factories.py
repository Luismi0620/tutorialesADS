import os

from .gateways import BancoNacionalProcesador


class MockPaymentProcessor:
    """Procesador liviano para desarrollo y pruebas."""

    def pagar(self, monto: float, contexto=None) -> bool:
        print(
            f"[DEBUG] Mock Payment: Procesando pago de ${monto} "
            "sin cargo real."
        )
        return True


class PaymentFactory:
    """Selecciona el procesador según la configuración del entorno."""

    @staticmethod
    def get_processor(tutorial_numero=1):
        provider = os.getenv("PAYMENT_PROVIDER", "BANCO").upper()

        if provider == "MOCK":
            return MockPaymentProcessor()

        return BancoNacionalProcesador(tutorial_numero=tutorial_numero)
