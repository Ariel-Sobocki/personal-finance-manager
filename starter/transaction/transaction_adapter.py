# PATRÓN DE DISEÑO: Adapter
# Permite que una clase con una interfaz "extranjera" funcione dentro del
# sistema sin modificar ninguna de las dos clases involucradas.
# Roles en este proyecto:
# - Adaptee (lo externo):  ExternalFreelanceIncome -> amount, invoice_id,
#                          description, typ ("income" como string).
# - Target (lo interno):   Transaction -> amount + category (Enum).
# - Adapter:               TransactionAdapter -> traduce Adaptee a Target.

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TransactionAdapter:
    def __init__(self, external_transaction):
        # Guarda el objeto externo que se va a adaptar (composición:
        # el adapter "envuelve" al objeto externo, no hereda de él).
        self.external_transaction = external_transaction

    def to_transaction(self):
        # Alias corto para no repetir self.external_transaction.
        ext = self.external_transaction
        # 1) TRADUCIR: el sistema externo usa un string ("income") y el
        #    sistema interno usa un Enum (TransactionCategory). Cualquier
        #    tipo desconocido se rechaza con ValueError, para no aplicar al
        #    saldo datos que no sabemos interpretar.
        if ext.typ == "income":
            category = TransactionCategory.INCOME
        else:
            raise ValueError(f"Tipo de transacción externa desconocido: {ext.typ}")
        # 2) CONSTRUIR: se crea la Transaction interna con el MONTO del objeto
        #    externo (ext.amount) y la categoría traducida. Los datos que el
        #    sistema no necesita (invoice_id, description) se descartan.
        return Transaction(ext.amount, category)
