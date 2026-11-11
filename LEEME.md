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
