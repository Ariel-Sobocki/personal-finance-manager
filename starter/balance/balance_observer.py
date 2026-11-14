# PATRÓN DE DISEÑO: Observer
# Define una relación "uno a muchos": cuando el Subject (Balance) cambia,
# notifica automáticamente a todos sus Observers suscriptos.
#
# Roles en este proyecto:
# - Subject:  Balance -> guarda la lista _observers, los suscribe con
#             register_observer() y los notifica en apply_transaction().
# - Observer: IBalanceObserver (interfaz) y sus implementaciones concretas
#             PrintObserver y LowBalanceAlertObserver.


class IBalanceObserver:
    # "Interfaz" de los observers: define el método que todo observer debe
    # tener. Si una subclase no implementa update(), al llamarlo se lanza
    # NotImplementedError.
    def update(self, balance, transaction):
        # balance:     el objeto Balance (Subject) que cambió.
        # transaction: la Transaction que se acaba de aplicar.
        raise NotImplementedError("Subclasses must implement update method.")


class PrintObserver(IBalanceObserver):
    # Observer concreto que muestra por pantalla cada actualización del saldo.
    def update(self, balance, transaction):
        """Print balance update message."""
        pass


class LowBalanceAlertObserver(IBalanceObserver):
    # Observer concreto que enciende una alerta cuando el saldo baja del umbral.
    def __init__(self, threshold):
        # threshold:       umbral mínimo de saldo (ej: 50).
        # alert_triggered: estado de la alerta; arranca apagada (False).
        self.threshold = threshold
        self.alert_triggered = False

    def update(self, balance, transaction):
        # Se recalcula en CADA notificación: la alerta se enciende si el saldo
        # es menor que el umbral y se apaga cuando el saldo se recupera.
        self.alert_triggered = balance.get_balance() < self.threshold
