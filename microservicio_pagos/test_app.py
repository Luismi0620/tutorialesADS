import unittest

from app import app


class PagosFlaskTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_compra_exitosa(self):
        response = self.client.post(
            "/api/v2/comprar",
            json={"producto_id": 1, "cantidad": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "Aprobado")
        self.assertIn("Microservicio Flask", response.get_json()["mensaje"])

    def test_compra_requiere_producto(self):
        response = self.client.post("/api/v2/comprar", json={"cantidad": 1})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Falta el ID del producto"},
        )


if __name__ == "__main__":
    unittest.main()
