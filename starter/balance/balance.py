# Módulo que contiene la clase Balance, responsable de llevar el saldo neto
# de la aplicación (ingresos - gastos).
#
# PATRÓN DE DISEÑO: Singleton
# - Garantiza que exista UNA ÚNICA instancia de Balance en toda la aplicación.
# - Ofrece un punto de acceso global a esa instancia: Balance.get_instance().
# - Motivo: si cada parte del programa creara su propio Balance, habría varios
#   saldos distintos y desincronizados.
from transaction.transaction_category import TransactionCategory


class Balance:
    """Singleton to track the balance."""
    # Atributo de CLASE (no de instancia): es compartido por toda la clase.
    # Guarda la única instancia de Balance. Empieza en None porque todavía
    # no se creó ninguna.
    _instance = None

    def __init__(self):
        # Constructor: se ejecuta al hacer Balance().
        # Si ya existe una instancia, se prohíbe crear otra lanzando un error.
        # Así se obliga a usar Balance.get_instance() como único acceso.
        if Balance._instance is not None:
            raise RuntimeError("Balance es un Singleton: usá Balance.get_instance()")
        self._balance = 0.0
        # Lista de observers suscriptos (patrón Observer): Balance es el
        # "Subject" y avisa a cada uno después de aplicar una transacción.
        self._observers = []

    @classmethod
    def get_instance(cls):
        """Return the single Balance instance, creating it if needed."""
        # Método de CLASE: recibe la clase (cls) en lugar de una instancia,
        # por eso se puede llamar como Balance.get_instance() sin tener un objeto.
        # - La primera vez: _instance es None -> se crea el objeto con cls()
        #   y se guarda en _instance.
        # - Las siguientes veces: se devuelve el MISMO objeto ya guardado.
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def reset(self):
        # Vuelve el saldo a cero.
        self._balance = 0.0

    def add_income(self, amount):
        # Suma un ingreso al saldo.
        self._balance += amount

    def add_expense(self, amount):
        # Resta un gasto del saldo.
        self._balance -= amount

    def apply_transaction(self, transaction):
        # Aplica una transacción completa según su categoría.
        # IMPORTANTE: el monto viene del parámetro (transaction.amount),
        # - INCOME  -> delega en add_income() (reutiliza código existente).
        # - EXPENSE -> delega en add_expense().
        # - Otra categoría -> ValueError, para no aplicar datos inválidos.
        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
        elif transaction.category == TransactionCategory.EXPENSE:
            self.add_expense(transaction.amount)
        else:
            raise ValueError("Categoría de transacción inválida")

        # Notifica a todos los observers suscriptos (patrón Observer).
        # Se hace DESPUÉS de actualizar el saldo, para que vean el valor nuevo.
        # Si la categoría es inválida, el raise corta antes y no se notifica.
        # Se pasa self (el Balance entero) para que el observer consulte lo
        # que necesite, por ejemplo balance.get_balance().
        for observer in self._observers:
            observer.update(self, transaction)

    def register_observer(self, observer):
        # Suscribe un observer: lo agrega a la lista para que reciba avisos.
        self._observers.append(observer)

    def get_balance(self):
        # Devuelve el saldo neto actual.
        return self._balance

    def summary(self):
        # Devuelve un texto legible con el saldo.
        # El formato :.2f muestra el número con 2 decimales (ej: 100.00).
        # Cubierto por el test propio test_summary.
        return f"Saldo neto: {self._balance:.2f}"
