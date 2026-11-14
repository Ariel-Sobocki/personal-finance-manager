"""This module serves as the entry point for the program."""
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver
from balance.balance_observer import PrintObserver
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_adapter import TransactionAdapter
from transaction.external_income_transaction import ExternalFreelanceIncome


def main():
    print("Adding transactions...")

    # SINGLETON: se obtiene la instancia única del saldo (nunca con Balance()).
    balance = Balance.get_instance()

    # OBSERVER: se suscriben los observers que reaccionan a cada transacción.
    # - PrintObserver: imprime cada transacción y el saldo resultante.
    # - LowBalanceAlertObserver: enciende una alerta si el saldo baja de 100.
    #   Se guarda en una variable para consultar su estado al final.
    alert_observer = LowBalanceAlertObserver(threshold=100)
    balance.register_observer(PrintObserver())
    balance.register_observer(alert_observer)

    # Create standard transactions
    transactions = [
        Transaction(100, TransactionCategory.INCOME),
        Transaction(50, TransactionCategory.EXPENSE),
        Transaction(200, TransactionCategory.INCOME),
        Transaction(75, TransactionCategory.EXPENSE),
    ]

    # ADAPTER: el ingreso freelance externo se convierte en una Transaction
    # interna para que Balance pueda procesarlo.
    freelance_income = ExternalFreelanceIncome(1200, "INV-98765", "Mobile App Project")
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()

    all_transactions = transactions + [adapted_transaction]

    # Se aplica cada transacción; Balance notifica a los observers en cada una.
    for t in all_transactions:
        balance.apply_transaction(t)

    # Resultado final: estado de la alerta (solo refleja el ÚLTIMO saldo) y resumen.

    print(f"Alerta de saldo bajo activa: {alert_observer.alert_triggered}")
    print(balance.summary())


if __name__ == "__main__":
    main()
