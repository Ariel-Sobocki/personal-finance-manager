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
