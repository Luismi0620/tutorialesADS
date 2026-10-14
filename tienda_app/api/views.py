import os

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tienda_app.infra.factories import PaymentFactory
from tienda_app.services import CompraService

from .serializers import OrdenInputSerializer


class CompraAPIView(APIView):
    """Procesa compras JSON reutilizando la misma capa de servicio."""

    def post(self, request):
        serializer = OrdenInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datos = serializer.validated_data

        try:
            tutorial_numero = int(os.getenv("TUTORIAL_NUMERO", "3"))
            gateway = PaymentFactory.get_processor(
                tutorial_numero=tutorial_numero
            )
            servicio = CompraService(procesador_pago=gateway)
            usuario = request.user if request.user.is_authenticated else None
            total = servicio.ejecutar_compra(
                libro_id=datos["libro_id"],
                cantidad=datos["cantidad"],
                direccion=datos["direccion_envio"],
                usuario=usuario,
            )
        except Http404 as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValueError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_409_CONFLICT,
            )
        except Exception:
            return Response(
                {"error": "Error interno"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "estado": "exito",
                "mensaje": f"Orden creada. Total: {total}",
            },
            status=status.HTTP_201_CREATED,
        )
