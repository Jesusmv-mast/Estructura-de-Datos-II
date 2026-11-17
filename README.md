# Estructura de Datos II

Repositorio de tareas y proyectos de la asignatura **Estructura de Datos II**.

## Proyectos

| Proyecto | Descripción | Tecnologías |
| --- | --- | --- |
| [arbol_expresion_mvc](proyectos/arbol_expresion_mvc/README.md) | Árbol de expresiones matemáticas con interfaz web | Python, Flask, MVC |
| [conecta_4](proyectos/conecta_4/README.md) | Juego Conecta 4 con IA basada en Minimax y árbol de decisión | Python, Tkinter, scikit-learn, MVC |

Los proyectos están en la carpeta [`proyectos/`](proyectos/README.md) para que se vean desde el inicio del repositorio.

## Organización por unidades

| Unidad | Tema | Contenido |
| --- | --- | --- |
| [Unidad 0](unidad0_estandares_y_buenas_practicas/) | Estándares y buenas prácticas de codificación | Guía de PEP 8 y ejemplo aplicado a una estructura de datos |
| [Unidad 1](unidad1_arboles_binarios_de_busqueda/) | Árboles binarios de búsqueda | Tareas de árboles binarios, AVL y árboles de expresión |
| [Unidad 2](unidad2_arboles_m_vias/) | Árboles M-vías | Investigación e implementación de un árbol M-vías |
| [Unidad 3](unidad3_arboles_b_y_b_plus/) | Árboles B y B+ | Investigación e implementaciones de árboles B y B+ |
| [Unidad 4](unidad4_grafos/) | Grafos | Representación con lista y matriz, DFS y BFS |
| [Unidad 5](unidad5_grafos_pesados/) | Grafos pesados | Dijkstra, Bellman-Ford, Kruskal y Prim |

Las prácticas entregadas se guardan en `tareas/` dentro de su unidad. Los algoritmos y ejemplos adicionales están en `algoritmos/`. Las carpetas se nombran por tema, sin numeración.

## Estructura del repositorio

```text
Estructura-de-Datos-II/
├── README.md
├── .gitignore
├── proyectos/
│   ├── README.md
│   ├── arbol_expresion_mvc/
│   └── conecta_4/
├── unidad0_estandares_y_buenas_practicas/
│   ├── README.md
│   └── tareas/
│       └── pep8/
├── unidad1_arboles_binarios_de_busqueda/
│   ├── README.md
│   └── tareas/
│       ├── tablero_tres_en_raya/
│       ├── arbol_binario_busqueda/
│       ├── arbol_avl/
│       └── arbol_de_expresiones/
├── unidad2_arboles_m_vias/
│   ├── README.md
│   ├── investigacion.md
│   └── algoritmos/
│       ├── README.md
│       └── arbol_m_vias.py
├── unidad3_arboles_b_y_b_plus/
│   ├── README.md
│   ├── investigacion.md
│   └── algoritmos/
│       ├── README.md
│       ├── arbol_b.py
│       └── arbol_b_plus.py
├── unidad4_grafos/
│   ├── README.md
│   └── algoritmos/
│       ├── README.md
│       ├── grafo.py
│       ├── dfs.py
│       └── bfs.py
└── unidad5_grafos_pesados/
    ├── README.md
    └── algoritmos/
        ├── README.md
        ├── dijkstra.py
        ├── bellman_ford.py
        ├── kruskal.py
        └── prim.py
```

## Cómo ejecutar los ejemplos

Cada ejemplo de Python se ejecuta desde su propia carpeta:

```bash
cd unidad1_arboles_binarios_de_busqueda/tareas/tablero_tres_en_raya
python arbol.py
```

```bash
cd unidad1_arboles_binarios_de_busqueda/tareas/arbol_binario_busqueda
python Arbol_recursivo.py
```

```bash
cd unidad0_estandares_y_buenas_practicas/tareas/pep8
python pila_pep8.py
```

```bash
cd unidad2_arboles_m_vias/algoritmos
python arbol_m_vias.py
```

```bash
cd unidad3_arboles_b_y_b_plus/algoritmos
python arbol_b.py
python arbol_b_plus.py
```

```bash
cd unidad4_grafos/algoritmos
python grafo.py
python dfs.py
python bfs.py
```

```bash
cd unidad5_grafos_pesados/algoritmos
python dijkstra.py
python bellman_ford.py
python kruskal.py
python prim.py
```

Las tareas y proyectos que usan dependencias externas incluyen su propio `requirements.txt`.

## Convenciones del repositorio

- Carpetas y archivos en minúsculas, separados con guiones bajos.
- Los nombres de las carpetas describen el tema, sin prefijos numéricos.
- Código Python nuevo siguiendo PEP 8 y PEP 257 (docstrings).
- El código importado de entregas anteriores se conserva tal como estaba; se irá ajustando cuando se revise.
- Cada tarea y proyecto debe tener un `README.md` que explique qué se hizo y cómo ejecutarlo.
- No se suben archivos generados como `__pycache__/`, `.pyc`, entornos virtuales ni cachés de pruebas.
