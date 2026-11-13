# Pruebas unitarias de la clase Transaction.
# Ejecutar desde starter/:  python3 -m unittest transaction/test_transaction.py -v
import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestTransaction(unittest.TestCase):

    def test_transaction_creation(self):
        # Verifica que el constructor guarde correctamente monto y categoría.
        t = Transaction(100, TransactionCategory.EXPENSE)
        self.assertEqual(t.amount, 100)
        self.assertEqual(t.category, TransactionCategory.EXPENSE)

    def test_transaction_str(self):
        # Verifica el texto exacto que devuelve __str__ (carácter por carácter).
        t = Transaction(50, TransactionCategory.INCOME)
        self.assertEqual(str(t), "Transaction($50, category='TransactionCategory.INCOME')")

    def test_transaction_equality(self):
        # Verifica la igualdad por valor (__eq__):
        # - t1 y t2 son objetos distintos con los mismos datos -> iguales.
        # - t1 y t3 tienen distinto monto -> distintos.
        t1 = Transaction(20, TransactionCategory.EXPENSE)
        t2 = Transaction(20, TransactionCategory.EXPENSE)
        t3 = Transaction(30, TransactionCategory.EXPENSE)
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)

    def test_transaction_not_equal_different_category(self):
        # PRUEBA PROPIA (tarea 5): mismo monto pero distinta categoría -> distintos.
        # Cubre un hueco del test original (que solo usaba EXPENSE): si se
        # borrara la comparación de categoría en __eq__, esta prueba fallaría.
        t1 = Transaction(20, TransactionCategory.EXPENSE)
        t2 = Transaction(20, TransactionCategory.INCOME)
        self.assertNotEqual(t1, t2)

    def test_transaction_not_equal_other_type(self):
        # PRUEBA PROPIA (tarea 5): comparar con un objeto que no es Transaction
        # debe dar "distinto" sin lanzar AttributeError (rama NotImplemented).
        t = Transaction(20, TransactionCategory.EXPENSE)
        self.assertNotEqual(t, "Transaction($20)")


# Permite ejecutar este archivo directamente: python3 transaction/test_transaction.py
if __name__ == "__main__":
    unittest.main()
