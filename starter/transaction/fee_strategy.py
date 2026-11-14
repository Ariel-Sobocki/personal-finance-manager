# fee_strategy.py
#
# PATRÓN DE DISEÑO: Strategy (cuarto patrón, elegido para la tarea 6)
# Define una familia de algoritmos intercambiables (reglas de comisión),
# cada uno en su propia clase, con la MISMA interfaz: apply_fee(amount).
#
# Roles en este proyecto:
# - Strategy (interfaz):   FeeStrategy -> apply_fee(amount).
# - Estrategias concretas: NoFeeStrategy (sin comisión) y
#                          PercentageFeeStrategy (descuenta un porcentaje).
# - Context (quien la usa): TransactionAdapter -> llama a apply_fee() sin
#                          saber qué estrategia concreta recibió.
#
# Ventaja: para agregar una regla nueva (ej: comisión fija de $50) se crea
# una clase nueva; el Adapter no cambia (principio abierto/cerrado).


class FeeStrategy:
    # Interfaz: toda estrategia de comisión debe tener apply_fee().
    def apply_fee(self, amount):
        raise NotImplementedError("Subclasses must implement apply_fee method.")


class NoFeeStrategy(FeeStrategy):
    # Estrategia concreta: no cobra comisión.
    def apply_fee(self, amount):
        return amount


class PercentageFeeStrategy(FeeStrategy):
    # Estrategia concreta: descuenta un porcentaje del monto.
    def __init__(self, percentage):
        # percentage: porcentaje de comisión (ej: 10 = 10%). Se guarda en el
        # objeto (self) para poder usarlo después en apply_fee().
        self.percentage = percentage

    def apply_fee(self, amount):
        # Monto neto = monto - comisión. Ej: 1200 - 1200 * 10 / 100 = 1080.0
        # El operador / siempre devuelve float en Python 3 (por eso el ".0").
        return amount - amount * self.percentage / 100
