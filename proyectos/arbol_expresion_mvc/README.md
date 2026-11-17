# Árbol de Expresión con MVC y Flask

## Descripción

Versión web del proyecto de árbol de expresiones usando el patrón **MVC** (Modelo-Vista-Controlador) y **Flask**. Permite cargar expresiones desde el navegador, ver su árbol, convertirlas a posfija, evaluarlas y descargar el resultado.

## Estructura

```text
arbol_expresion_mvc/
├── app.py
├── requirements.txt
├── Controllers/
│   └── arbol_controller.py
├── Models/
│   ├── Arbol_expresion.py
│   ├── Nodo.py
│   ├── Tokenizador.py
│   └── Validador.py
├── Static/
│   └── style.css
└── Templates/
    └── index.html
```

| Componente | Responsabilidad |
| --- | --- |
| `Models/` | Lógica del árbol, tokenización y validación |
| `Controllers/` | Rutas y control de las acciones del usuario |
| `Templates/` | Vista HTML |
| `Static/` | Estilos de la página |

## Cómo ejecutar

Desde esta carpeta:

```bash
pip install -r requirements.txt
python app.py
```

Luego abrir en el navegador:

```text
http://127.0.0.1:5000
```

## Dependencias

- Flask.

## Nota

La aplicación usa `session` para guardar las expresiones cargadas mientras el navegador mantiene la sesión.
