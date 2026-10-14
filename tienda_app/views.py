from django.views import View
from django.shortcuts import render

from .infra.factories import PaymentFactory
from .services import CompraService

class CompraView(View):
    template_name = 'tienda_app/compra.html'

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
            return render(
                request,
                self.template_name,
                {
                    'mensaje_exito': f"¡Gracias por su compra! Total: ${total}",
                    'total': total,
                },
            )
        except Exception as error:
            return render(
                request,
                self.template_name,
                {'error': str(error)},
                status=400,
            )
