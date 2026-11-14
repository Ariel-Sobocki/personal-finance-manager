# Pruebas unitarias del patrón Observer (LowBalanceAlertObserver y PrintObserver).
import io                                  # StringIO: "pantalla falsa" en memoria
from contextlib import redirect_stdout     # redirige los print() a otro destino
import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintObserver


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

class TestPrintObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_print_observer_prints_transaction_and_balance(self):
        # PRUEBA PROPIA (tarea 5): verifica el mensaje que imprime PrintObserver.
        observer = PrintObserver()
        self.balance.register_observer(observer)

        output = io.StringIO()                 # "pantalla falsa" en memoria
        with redirect_stdout(output):          # todo print() va a parar a output
            self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))

        self.assertEqual(
            output.getvalue().strip(),         # .strip() quita el salto de línea final
            "Transaction($100, category='TransactionCategory.INCOME') -> Saldo neto: 100.00",
        )


# Permite ejecutar este archivo directamente: python3 balance/test_balance_observer.py
if __name__ == "__main__":
    unittest.main()
