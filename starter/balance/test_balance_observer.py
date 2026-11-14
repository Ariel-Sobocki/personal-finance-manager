# Pruebas unitarias del patrón Observer (LowBalanceAlertObserver).

import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver


class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        # Obtiene la instancia única (Singleton) y devuelve el saldo a 0.0.
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_alert_triggers_on_low_balance(self):
        # Verifica que la alerta se RECALCULE en cada transacción (umbral = 50):
        # se enciende cuando el saldo baja de 50 y se apaga cuando se recupera.
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))   # saldo 100
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))   # saldo 40 -> alerta
        self.assertTrue(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))   # saldo 140
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))   # saldo 80
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))   # saldo 20 -> alerta
        self.assertTrue(observer.alert_triggered)


# Permite ejecutar este archivo directamente: python3 balance/test_balance_observer.py
if __name__ == "__main__":
    unittest.main()
