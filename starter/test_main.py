# Prueba de aceptación: ejecuta main() completo y verifica el saldo final.
import io
import unittest
from contextlib import redirect_stdout
from balance.balance import Balance
import main


class TestMain(unittest.TestCase):
    def setUp(self):
        # main() usa el Singleton: se arranca con una instancia NUEVA (saldo 0,
        # sin observers) y se descarta al terminar, para no afectar otros tests.
        Balance._instance = None
        self.addCleanup(setattr, Balance, "_instance", None)

    def test_main_applies_all_transactions(self):
        output = io.StringIO()
        with redirect_stdout(output):
            main.main()
        text = output.getvalue()
        lines = text.strip().splitlines()

        self.assertEqual(lines[-1], "Saldo neto: 1255.00")   # 100-50+200-75+1080 (1200 - 10%)
        self.assertIn("Transaction($1080", text)              # el ingreso adaptado, neto de comisión


if __name__ == "__main__":
    unittest.main()
