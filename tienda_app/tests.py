import os
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import TestCase, override_settings

from .domain.builders import OrdenBuilder
from .infra.factories import MockPaymentProcessor, PaymentFactory
from .infra.gateways import BancoNacionalProcesador
from .models import Inventario, Libro, Orden
from .services import CompraService


class PatronesCreacionalesTests(TestCase):
    def setUp(self):
        self.libro = Libro.objects.create(titulo="Clean Code", precio="100.00")
        Inventario.objects.create(libro=self.libro, cantidad=3)

    def test_factory_usa_banco_por_defecto(self):
        with patch.dict(os.environ, {}, clear=True):
            procesador = PaymentFactory.get_processor()

        self.assertIsInstance(procesador, BancoNacionalProcesador)
        self.assertEqual(procesador.tutorial_numero, 1)

    def test_factory_separa_el_log_del_tutorial_tres(self):
        with patch.dict(os.environ, {}, clear=True):
            procesador = PaymentFactory.get_processor(tutorial_numero=3)

        self.assertIsInstance(procesador, BancoNacionalProcesador)
        self.assertEqual(procesador.tutorial_numero, 3)

    def test_log_tutorial_tres_incluye_cambio_de_inventario(self):
        with TemporaryDirectory() as directorio_temporal:
            with override_settings(BASE_DIR=Path(directorio_temporal)):
                servicio = CompraService(
                    PaymentFactory.get_processor(tutorial_numero=3)
                )
                servicio.ejecutar_compra(self.libro.id)
                contenido = (
                    Path(directorio_temporal) / "pagos_tutorial03_MIRAL.log"
                ).read_text(encoding="utf-8")

        self.assertIn("Libro:", contenido)
        self.assertIn("Inventario: 3 -> 2", contenido)

    def test_factory_usa_mock_segun_variable_de_entorno(self):
        with patch.dict(os.environ, {"PAYMENT_PROVIDER": "MOCK"}):
            self.assertIsInstance(
                PaymentFactory.get_processor(), MockPaymentProcessor
            )

    def test_builder_crea_orden_y_se_reinicia(self):
        builder = OrdenBuilder()
        orden = (
            builder.con_libro(self.libro)
            .con_cantidad(2)
            .para_envio("Calle 123")
            .build()
        )

        self.assertEqual(orden.total, 238)
        self.assertEqual(orden.direccion_envio, "Calle 123")
        with self.assertRaisesMessage(ValueError, "Datos insuficientes"):
            builder.build()

    def test_service_integra_builder_y_factory_mock(self):
        with patch.dict(os.environ, {"PAYMENT_PROVIDER": "MOCK"}):
            servicio = CompraService(PaymentFactory.get_processor())
            with patch("sys.stdout", new_callable=StringIO) as salida:
                total = servicio.ejecutar_compra(self.libro.id)

        self.assertEqual(total, 119)
        self.assertIn("[DEBUG] Mock Payment", salida.getvalue())
        self.assertEqual(Orden.objects.count(), 1)
        self.assertEqual(Inventario.objects.get(libro=self.libro).cantidad, 2)

    def test_vista_delega_la_compra_al_servicio(self):
        with patch.dict(os.environ, {"PAYMENT_PROVIDER": "MOCK"}):
            respuesta_get = self.client.get(f"/compra/{self.libro.id}/")
            with patch("sys.stdout", new_callable=StringIO):
                respuesta_post = self.client.post(f"/compra/{self.libro.id}/")

        self.assertEqual(respuesta_get.status_code, 200)
        self.assertContains(respuesta_get, "Clean Code")
        self.assertEqual(respuesta_post.status_code, 200)
        self.assertContains(respuesta_post, "Gracias por su compra")


class CompraAPITests(TestCase):
    def setUp(self):
        self.libro = Libro.objects.create(titulo="API Design", precio="80.00")
        Inventario.objects.create(libro=self.libro, cantidad=3)
        self.url = "/api/v1/comprar/"

    def test_api_reutiliza_servicio_y_descuenta_inventario(self):
        payload = {
            "libro_id": self.libro.id,
            "direccion_envio": "Calle API 123",
            "cantidad": 2,
        }

        with patch.dict(os.environ, {"PAYMENT_PROVIDER": "MOCK"}):
            with patch("sys.stdout", new_callable=StringIO):
                respuesta = self.client.post(
                    self.url,
                    data=payload,
                    content_type="application/json",
                )

        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.json()["estado"], "exito")
        self.assertEqual(Inventario.objects.get(libro=self.libro).cantidad, 1)
        self.assertEqual(Orden.objects.filter(libro=self.libro).count(), 1)

        respuesta_html = self.client.get(f"/compra/{self.libro.id}/")
        self.assertContains(respuesta_html, "Stock disponible")
        self.assertContains(respuesta_html, "<strong>1</strong>", html=True)

    def test_api_rechaza_payload_invalido(self):
        respuesta = self.client.post(
            self.url,
            data={"libro_id": 0, "direccion_envio": ""},
            content_type="application/json",
        )

        self.assertEqual(respuesta.status_code, 400)
        self.assertIn("libro_id", respuesta.json())
        self.assertIn("direccion_envio", respuesta.json())

    def test_api_devuelve_conflicto_sin_stock(self):
        payload = {
            "libro_id": self.libro.id,
            "direccion_envio": "Calle API 123",
            "cantidad": 4,
        }

        with patch.dict(os.environ, {"PAYMENT_PROVIDER": "MOCK"}):
            respuesta = self.client.post(
                self.url,
                data=payload,
                content_type="application/json",
            )

        self.assertEqual(respuesta.status_code, 409)
        self.assertIn("stock", respuesta.json()["error"])

    def test_api_lista_productos_desde_django_v1(self):
        respuesta = self.client.get("/api/v1/productos/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.json()), 1)
        self.assertEqual(respuesta.json()[0]["titulo"], "API Design")
        self.assertEqual(respuesta.json()[0]["stock_actual"], 3)

# Create your tests here.
