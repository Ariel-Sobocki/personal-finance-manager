# Pruebas unitarias del patrón Adapter (TransactionAdapter).
# Ejecutar desde starter/:  python3 -m unittest transaction/test_transaction_adapter.py -v

import unittest
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestTransactionAdapter(unittest.TestCase):
    def test_adapter_converts_freelance_income(self):
        # Verifica que un ingreso freelance externo se convierta en una
        # Transaction interna equivalente (mismo monto, categoría INCOME).
        # assertEqual funciona gracias a Transaction.__eq__ (Paso 4).
        ext_txn = ExternalFreelanceIncome(500, "INV-12345", "Website development")
        adapter = TransactionAdapter(ext_txn)
        txn = adapter.to_transaction()
        self.assertEqual(txn, Transaction(500, TransactionCategory.INCOME))

    def test_adapter_rejects_unknown_type(self):
        # PRUEBA PROPIA (tarea 5): si la plataforma externa envía un tipo
        # desconocido, el adapter debe lanzar ValueError en lugar de
        # convertirlo silenciosamente en un ingreso.
        ext_txn = ExternalFreelanceIncome(500, "INV-99999", "Reembolso")
        ext_txn.typ = "refund"   # simulamos que la plataforma manda un tipo desconocido
        adapter = TransactionAdapter(ext_txn)
        with self.assertRaises(ValueError):
            adapter.to_transaction()


# Permite ejecutar este archivo directamente: python3 transaction/test_transaction_adapter.py
if __name__ == "__main__":
    unittest.main()
