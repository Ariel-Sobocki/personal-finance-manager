# test_fee_strategy.py
# Pruebas unitarias del patrón Strategy (estrategias de comisión).
import unittest
from transaction.fee_strategy import NoFeeStrategy, PercentageFeeStrategy


class TestFeeStrategy(unittest.TestCase):

    def test_no_fee_keeps_amount(self):
        # Sin comisión: el monto queda igual.
        strategy = NoFeeStrategy()
        self.assertEqual(strategy.apply_fee(1200), 1200)

    def test_percentage_fee_discounts_amount(self):
        # Comisión del 10%: 1200 - 120 = 1080.
        strategy = PercentageFeeStrategy(10)
        self.assertEqual(strategy.apply_fee(1200), 1080)


if __name__ == "__main__":
    unittest.main()
