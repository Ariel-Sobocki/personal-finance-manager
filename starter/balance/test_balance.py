# Pruebas unitarias de la clase Balance (patrón Singleton).

import unittest
from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


# Clase de pruebas: hereda de unittest.TestCase. Cada método que empieza
# con "test_" es una prueba independiente que unittest ejecuta automáticamente.
class TestBalance(unittest.TestCase):

    def setUp(self):
        # Se ejecuta ANTES de cada prueba.
        # Obtiene la instancia única y reinicia el saldo a 0.0, porque al ser
        # Singleton el estado se conservaría de una prueba a la siguiente.
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_initial_balance(self):
        # Verifica que el saldo inicial (tras reset) sea 0.0.
        self.assertEqual(self.balance.get_balance(), 0.0)

    def test_singleton_instance(self):
        # Verifica el núcleo del Singleton: dos llamadas a get_instance()
        # devuelven el MISMO objeto. assertIs compara identidad (misma
        # posición en memoria), no solo igualdad de valores.
        balance1 = Balance.get_instance()
        balance2 = Balance.get_instance()
        self.assertIs(balance1, balance2)

    def test_add_income(self):
        # Verifica que add_income sume el monto al saldo.
        self.balance.add_income(100)
        self.assertEqual(self.balance.get_balance(), 100)

    def test_add_expense(self):
        # Verifica que add_expense reste el monto (el saldo puede quedar negativo).
        self.balance.add_expense(40)
        self.assertEqual(self.balance.get_balance(), -40)

    def test_apply_transaction_income(self):
        # Verifica que una transacción INCOME aumente el saldo en su monto.
        t = Transaction(150, TransactionCategory.INCOME)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), 150)

    def test_apply_transaction_expense(self):
        # Verifica que una transacción EXPENSE disminuya el saldo en su monto.
        t = Transaction(60, TransactionCategory.EXPENSE)
        self.balance.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), -60)

    def test_apply_transaction_invalid_category(self):
        # Verifica que una categoría desconocida lance ValueError.
        # FakeCategory es una clase "falsa" que no es INCOME ni EXPENSE.
        # assertRaises usado como "with" pasa solo si el bloque lanza el error.
        class FakeCategory:
            pass
        t = Transaction(100, FakeCategory())
        with self.assertRaises(ValueError):
            self.balance.apply_transaction(t)

    def test_reset(self):
        # Verifica que reset() vuelva el saldo a 0.0 después de operar.
        self.balance.add_income(100)
        self.balance.add_expense(50)
        self.balance.reset()
        self.assertEqual(self.balance.get_balance(), 0.0)

    def test_summary(self):
        # PRUEBA PROPIA (tarea 5): prueba de regresión del bug de formato
        # en summary() Verifica el texto exacto, con 2 decimales y sin espacios extra.
        self.balance.add_income(100)
        self.assertEqual(self.balance.summary(), "Saldo neto: 100.00")


# Permite ejecutar este archivo directamente: python3 balance/test_balance.py
if __name__ == "__main__":
    unittest.main()
