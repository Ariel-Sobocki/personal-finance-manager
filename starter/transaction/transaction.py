# Módulo que contiene la clase Transaction: representa una operación
# financiera individual (un ingreso o un gasto) con un monto y una categoría.
#
# Es el objeto "interno" del sistema: Balance lo consume en apply_transaction()
# y el Adapter (TransactionAdapter) convierte datos externos en Transaction.
from transaction.transaction_category import TransactionCategory


class Transaction:
    def __init__(self, amount, category: TransactionCategory):
        # Constructor: guarda los datos de la transacción.
        # amount:   monto de la operación (número positivo; el signo lo da la categoría).
        # category: TransactionCategory.INCOME (ingreso) o EXPENSE (gasto).
        self.amount = amount
        self.category = category

    def __str__(self):
        # Método especial ("dunder"): Python lo llama automáticamente al hacer
        # str(t) o print(t). Devuelve una representación legible del objeto.
        return f"Transaction(${self.amount}, category='{self.category}')"

    def __eq__(self, other):
        # Método especial: Python lo llama al hacer t1 == t2 (y assertEqual).
        # Por defecto Python compara IDENTIDAD (mismo objeto en memoria);
        # acá se define igualdad POR VALOR: dos transacciones son iguales si
        # tienen el mismo monto Y la misma categoría.
        # Si "other" no es una Transaction (ej: un string), no tiene .amount;
        # se devuelve NotImplemented para que Python resuelva la comparación
        # (termina dando False) en lugar de lanzar AttributeError.
        if not isinstance(other, Transaction):
            return NotImplemented
        return (self.amount == other.amount) and (self.category == other.category)
