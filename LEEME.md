# Registro de Actividades — Gestor de Finanzas Personales

Este documento registra, paso a paso, las actividades realizadas para dejar en correcto funcionamiento la aplicación del proyecto de Patrones de Diseño.
El desarrollo sigue la metodología TDD (Test-Driven Development): primero se escribe o se hace visible una prueba que falla (rojo), luego se implementa el código mínimo para que pase (verde) y finalmente se mejora el diseño sin romper las pruebas (refactor).

## Paso 1: Publicar el proyecto en GitHub personal

### Objetivo

Guardar el proyecto clonado desde la cuenta de Udacity en un repositorio propio, conservando la referencia al repositorio original.

### Descripción

1. Se renombró el remoto original de Udacity de `origin` a `upstream`, para conservarlo y poder traer futuras actualizaciones:

```
bash
git remote rename origin upstream
```

2. Se creó un archivo `.gitignore` para excluir del control de versiones los archivos generados automáticamente por Python y el editor:

```
bash
printf "__pycache__/\n*.pyc\n.venv/\n.vscode/\n" > .gitignore
git add .gitignore
git commit -m "chore: add .gitignore for Python artifacts"
```

3. Se creó el repositorio público `personal-finance-manager` en la cuenta personal de GitHub y se subió el proyecto:

```
bash
gh repo create personal-finance-manager --public --source=. --remote=origin --push
```

### Resultado

- `origin` → https://github.com/Ariel-Sobocki/personal-finance-manager.git (repositorio personal)
- `upstream` → https://github.com/udacity/cd14600-project-starter.git (repositorio original de Udacity)

### Observaciones

- Al ejecutar `python -m unittest discover` dentro de `starter/` el resultado fue `Ran 0 tests` con estado `OK`. Esto es una falsa sensación de seguridad: las pruebas existen pero no se están ejecutando. Se resolverá en el Paso 2.

## Paso 2: Hacer visibles las pruebas para unittest (fase ROJA)

### Objetivo

Lograr que `python -m unittest discover` encuentre y ejecute todas las pruebas existentes, para obtener un estado ROJO real desde el cual aplicar TDD.

### Descripción

1. Se identificó la causa de `Ran 0 tests`: `unittest discover` solo recorre carpetas que son *paquetes* de Python, es decir, que contienen un archivo `__init__.py`. Las carpetas `balance/` y `transaction/` no lo tenían.

2. Se crearon los archivos `__init__.py` vacíos:

```
bash
cd starter
touch balance/__init__.py transaction/__init__.py
```

3. Se volvieron a ejecutar todas las pruebas en modo detallado:

```
bash
python3 -m unittest discover -v
```

### Resultado

```
Ran 13 tests in 0.002s

FAILED (failures=2, errors=10)
```

- 1 prueba pasa: `test_transaction_creation`.
- 10 pruebas con `ERROR`: 9 por `AttributeError: type object 'Balance' has no attribute 'get_instance'` (falta el Singleton) y 1 por `TypeError: __str__ returned non-string` (falta `Transaction.__str__`).
- 2 pruebas con `FAIL`: `test_transaction_equality` (falta `Transaction.__eq__`) y `test_adapter_converts_freelance_income` (el Adapter devuelve `None`).

### Observaciones

- **ERROR vs FAIL:** un `ERROR` indica que el código lanzó una excepción inesperada antes de poder verificar el resultado (por ejemplo, un método inexistente). Un `FAIL` indica que el código se ejecutó, pero una aserción (`assertEqual`, `assertIs`, etc.) no se cumplió.
- Este es el punto de partida ROJO del ciclo TDD: a partir de aquí cada paso busca convertir pruebas en verde.

## Paso 3: Patrón Singleton — clase Balance

### Objetivo

Implementar la clase `Balance` como Singleton, garantizando que exista un único objeto de saldo en toda la aplicación, y completar sus operaciones de ingreso, gasto, aplicación de transacciones y resumen.

### Descripción

1. Se analizaron las pruebas de `balance/test_balance.py` como especificación: requieren el método de clase `Balance.get_instance()`, saldo inicial `0.0`, `reset()`, `add_income()`, `add_expense()`, `apply_transaction()` (con `ValueError` para categorías inválidas) y `get_balance()`.

2. Se descartó el enfoque con `__new__`: aunque es un Singleton válido en Python, las pruebas exigen `get_instance()` y además `__init__` se ejecuta en cada llamada a `Balance()`, lo que reiniciaría el saldo.

3. Se implementó el Singleton con un atributo de clase `_instance`, un `@classmethod get_instance()` que crea la instancia solo la primera vez, y un `__init__` que lanza `RuntimeError` si se intenta instanciar directamente cuando ya existe una instancia:

```
python
@classmethod
def get_instance(cls):
    if cls._instance is None:
        cls._instance = cls()
    return cls._instance
```

4. Se completaron los métodos del saldo. `apply_transaction()` delega en `add_income()` / `add_expense()` usando `transaction.amount`, y `summary()` devuelve `"Saldo neto: {saldo:.2f}"`.

5. Se ejecutaron las pruebas del módulo:

```
bash
python3 -m unittest balance/test_balance.py -v
```

6. Se agregó una prueba propia, `test_summary`, como prueba de regresión del bug de formato en `summary()`:

```
python
def test_summary(self):
    self.balance.add_income(100)
    self.assertEqual(self.balance.summary(), "Saldo neto: 100.00")
```

7. Se documentó el código con comentarios `#` en `balance/balance.py` (propósito del patrón Singleton, cada atributo y cada método), en `balance/test_balance.py` (qué verifica cada prueba) y en los archivos `__init__.py` (por qué existen).

### Resultado

```
Ran 9 tests in 0.000s

OK
```

### Observaciones

- **Shadowing:** asignar `self.get_balance = 0.0` en `__init__` tapaba el método `get_balance()` con un float, provocando `TypeError: 'float' object is not callable`. Se resolvió guardando el dato en el atributo interno `self._balance`.
- **Saldo vs. monto:** en `apply_transaction()` el valor a sumar o restar es el monto de la transacción recibida (`transaction.amount`), no el saldo actual (`self._balance` / `self.get_balance()`).
- **Bug no cubierto por pruebas:** el formato `{:2.f}` en `summary()` lanzaba `ValueError: Format specifier missing precision`, pero ninguna prueba llamaba a `summary()`. Esto evidencia la necesidad de escribir pruebas propias (tarea 5 del proyecto).
- **Buena práctica TDD:** se pueden *agregar* pruebas nuevas, pero no se deben modificar las existentes para que pasen.

## Paso 4: Completar la clase Transaction

### Objetivo

Implementar los métodos especiales `__str__` y `__eq__` de la clase `Transaction`, para que las transacciones puedan mostrarse como texto y compararse por valor.

### Descripción

1. Se ejecutaron las pruebas de `transaction/test_transaction.py` para ver el estado ROJO: `test_transaction_str` daba `ERROR` (`__str__` devolvía `None`) y `test_transaction_equality` daba `FAIL` (`__eq__` devolvía `None`).

2. Se implementó `__str__` con un f-string que respeta exactamente el formato exigido por la prueba:

```
python
def __str__(self):
    return f"Transaction(${self.amount}, category='{self.category}')"
```

3. Se implementó `__eq__` con igualdad por valor (mismo monto y misma categoría), devolviendo `NotImplemented` cuando el otro objeto no es una `Transaction`:

```
python
def __eq__(self, other):
    if not isinstance(other, Transaction):
        return NotImplemented
    return (self.amount == other.amount) and (self.category == other.category)
```

4. Se agregaron dos pruebas propias para cubrir huecos de las pruebas originales:
   - `test_transaction_not_equal_different_category`: mismo monto, distinta categoría.
   - `test_transaction_not_equal_other_type`: comparación contra un objeto que no es `Transaction`.

5. Se verificó que las pruebas nuevas detectan errores reales: al borrar temporalmente la comparación de categoría en `__eq__`, falló `test_transaction_not_equal_different_category`. Luego se restauró el código.

6. Se documentó el código con comentarios `#` en `transaction/transaction.py` y `transaction/test_transaction.py`.

```
bash
python3 -m unittest transaction/test_transaction.py -v
```

### Resultado

```
Ran 5 tests in 0.000s

OK
```

### Observaciones

- **Precedencia de operadores:** la primera versión `return self.amount and self.category == other` se evaluaba como `self.amount and (self.category == other)`, comparando una categoría contra una transacción entera y devolviendo siempre `False`. Cada lado del `and` debe ser una comparación completa entre atributos.
- **Tests que pasan por casualidad:** con ese bug, `assertNotEqual(t1, t3)` pasaba igual, porque el código devolvía siempre `False`. Por eso una prueba debe verificar tanto el caso "igual" como el caso "distinto".
- **Métodos especiales (dunder):** `__str__` y `__eq__` no se llaman directamente; Python los invoca al usar `str()` / `print()` y el operador `==`.

## Paso 5: Patrón Adapter — TransactionAdapter

### Objetivo

Adaptar los ingresos provenientes de una plataforma freelance externa (`ExternalFreelanceIncome`) a objetos internos `Transaction`, sin modificar ninguna de las dos clases.

### Descripción

1. Se identificaron los roles del patrón:
   - **Adaptee:** `ExternalFreelanceIncome` (`amount`, `invoice_id`, `description`, `typ = "income"`).
   - **Target:** `Transaction` (`amount` + `category` como Enum).
   - **Adapter:** `TransactionAdapter`, que recibe el objeto externo y devuelve una `Transaction`.

2. Se eligió una traducción robusta del tipo: el string `"income"` se traduce a `TransactionCategory.INCOME` y cualquier otro valor lanza `ValueError`.

3. Siguiendo TDD, primero se escribió la prueba propia `test_adapter_rejects_unknown_type` (ROJO) y luego se implementó `to_transaction()` (VERDE):

```
python
def to_transaction(self):
    ext = self.external_transaction
    if ext.typ == "income":
        category = TransactionCategory.INCOME
    else:
        raise ValueError(f"Tipo de transacción externa desconocido: {ext.typ}")
    return Transaction(ext.amount, category)
```

4. Se documentó el código con comentarios `#` en `transaction/transaction_adapter.py` y `transaction/test_transaction_adapter.py`.

```
bash
python3 -m unittest transaction/test_transaction_adapter.py -v
```

### Resultado

```
Ran 2 tests in 0.000s

OK
```

### Observaciones

- **Monto vs. tipo vs. objeto:** en las primeras versiones se pasó `ext.typ` y luego `ext` (el objeto entero) como monto de la `Transaction`. El monto correcto es el atributo `ext.amount`. Es el mismo error conceptual del Paso 3: distinguir el objeto de sus atributos.
- **Dependencia entre pasos:** la prueba del adapter compara con `assertEqual` dos objetos `Transaction` distintos; solo puede pasar gracias al `__eq__` implementado en el Paso 4.
- **Mensajes de error poco claros:** el `AssertionError` mostraba `<Transaction object at 0x...>` porque `assertEqual` usa `__repr__`, no `__str__`. Queda como mejora (refactor) agregar `__repr__` a `Transaction`.
- Los datos que el sistema interno no necesita (`invoice_id`, `description`) se descartan en la adaptación.

## Paso 6: Patrón Observer — LowBalanceAlertObserver

### Objetivo

Implementar el patrón Observer para que `Balance` notifique automáticamente a sus observadores después de cada transacción, y crear un observador que active una alerta cuando el saldo baja de un umbral.

### Descripción

1. Se analizó la prueba `balance/test_balance_observer.py` con una prueba de escritorio (umbral = 50): la alerta debe **recalcularse** en cada transacción, encendiéndose cuando el saldo es menor que 50 y apagándose cuando se recupera.

2. Se identificaron los roles del patrón:
   - **Subject:** `Balance`.
   - **Observer:** `IBalanceObserver` (interfaz), con las implementaciones `LowBalanceAlertObserver` y `PrintObserver`.

3. Se implementó en pasos pequeños, observando cómo cambiaba el error en cada uno:
   - **Cambio 1:** lista `self._observers = []` en `Balance.__init__` y método `register_observer()`. El error pasó de `no attribute 'register_observer'` a `no attribute 'alert_triggered'`.
   - **Cambio 2:** al final de `apply_transaction()`, después de actualizar el saldo, se notifica a cada observer con `observer.update(self, transaction)`.
   - **Cambio 3:** en `LowBalanceAlertObserver` se agregó `self.alert_triggered = False` y la lógica de `update()`:

```
python
def update(self, balance, transaction):
    self.alert_triggered = balance.get_balance() < self.threshold
```

4. Se documentó el código con comentarios `#` en `balance/balance.py`, `balance/balance_observer.py` y `balance/test_balance_observer.py`.

```
bash
python3 -m unittest discover
```

### Resultado

```
Ran 17 tests in 0.001s

OK
```

Todas las pruebas originales de Udacity (13) y las pruebas propias (4) pasan.

### Observaciones

- **Avanzar empujando el error:** en TDD, que el mensaje de error cambie es progreso. Cada cambio pequeño hizo que la prueba llegara un poco más lejos.
- **Notificar después de actualizar:** si se notificara antes, los observers verían el saldo viejo. Si la categoría es inválida, el `raise` corta la ejecución y nadie es notificado.
- **Se pasa el objeto Balance (`self`) a `update()`:** el observer le pide el número con `balance.get_balance()`. Una comparación ya devuelve `True` o `False`, por lo que no hace falta un `if`.
- **Pendientes detectados:**
  - `PrintObserver.update()` sigue sin implementar y ninguna prueba lo cubre.
  - **Singleton + Observer:** al terminar las pruebas queda 1 observer registrado en la instancia única, porque `reset()` solo reinicia el saldo. Los observers se acumulan entre pruebas.
  - `main.py` todavía tiene los `TODO` sin resolver: la aplicación solo imprime `Adding transactions...`.

## Paso 7: PrintObserver con TDD completo

### Objetivo

Implementar `PrintObserver`, que muestra por pantalla cada transacción aplicada y el saldo resultante, escribiendo primero una prueba propia (no existía prueba de Udacity para este observer).

### Descripción

1. Se diseñó el formato del mensaje reutilizando métodos ya probados: `Transaction.__str__` (Paso 4) y `Balance.summary()` (Paso 3):

```
Transaction($100, category='TransactionCategory.INCOME') -> Saldo neto: 100.00
```

2. **ROJO:** se escribió la prueba `TestPrintObserver.test_print_observer_prints_transaction_and_balance` en `balance/test_balance_observer.py`. Para capturar lo que imprime `print()` se usó `io.StringIO` como "pantalla falsa" y `contextlib.redirect_stdout`. Resultado: `AssertionError: '' != "Transaction(...) -> Saldo neto: 100.00"`.

3. **VERDE:** se implementó `update()`:

```
python
def update(self, balance, transaction):
    print(f"{transaction} -> {balance.summary()}")
```

4. Se documentó el código con comentarios `#`.

```
bash
python3 -m unittest discover
```

### Resultado

```
Ran 18 tests in 0.001s

OK
```

### Observaciones

- **Leer el diff del error:** `assertEqual` con strings muestra una línea `-` (lo obtenido) y una `+` (lo esperado), lo que permite ubicar la diferencia exacta.
- **Objeto vs. texto en un f-string:** `{transaction}` funciona porque `Transaction` tiene `__str__`; `{balance}` mostraba `<balance.balance.Balance object at 0x...>` porque `Balance` no lo tiene. La solución fue pedirle el texto con `balance.summary()` (con paréntesis, para *llamar* al método).
- **Trampa Singleton + Observer confirmada:** al terminar las pruebas quedan 2 observers registrados en la instancia única (`LowBalanceAlertObserver` y `PrintObserver`).

## Paso 8: Trampa Singleton + Observer — desuscripción de observers

### Objetivo

Evitar que los observers registrados en una prueba queden "colgados" en la instancia única de `Balance` y afecten a las pruebas siguientes.

### Descripción

1. Se detectó el problema: al terminar las pruebas quedaban registrados `LowBalanceAlertObserver` y `PrintObserver`, porque `Balance` es un Singleton (la lista `_observers` sobrevive entre pruebas) y `reset()` solo reinicia el saldo.

2. Se evaluaron dos opciones:
   - **A:** que `reset()` también vacíe `_observers`.
   - **B:** agregar `unregister_observer()` y que cada prueba desuscriba lo que suscribió.

   Se eligió la **opción B**: respeta la responsabilidad única de `reset()` (solo el saldo), evita desactivar alertas por accidente en `main.py` y completa el patrón Observer con la operación de desuscripción.

3. **ROJO:** se escribió la prueba propia `test_unregistered_observer_is_not_notified`: un observer desuscripto no debe encender la alerta aunque el saldo quede en -60. Resultado: `AttributeError: 'Balance' object has no attribute 'unregister_observer'`.

4. **VERDE:** se implementó el método en `Balance`:

```
python
def unregister_observer(self, observer):
    self._observers.remove(observer)
```

5. **Limpieza de pruebas:** en las pruebas que suscriben observers se agregó, justo después de `register_observer()`:

```
python
self.addCleanup(self.balance.unregister_observer, observer)
```

### Resultado

```
Ran 19 tests in 0.001s

OK
```

Al terminar todas las pruebas, la lista de observers de la instancia única queda vacía (`[]`).

### Observaciones

- **Pruebas dependientes del orden:** un estado compartido (Singleton) que no se limpia puede hacer que una prueba pase o falle según qué pruebas corrieron antes. Son errores muy difíciles de diagnosticar.
- **`addCleanup` vs. última línea:** `addCleanup` se ejecuta aunque la prueba falle; un `unregister_observer()` al final de la prueba no se ejecutaría si un `assert` previo falla.
- **Pasar un método sin paréntesis:** en `addCleanup` se pasa `self.balance.unregister_observer` (el método, para que unittest lo llame después), no `unregister_observer()` (que lo ejecutaría en ese momento).
