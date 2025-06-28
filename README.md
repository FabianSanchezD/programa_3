# Kakuro

**Juego de lógica de tipo crucigrama numérico hecho en Python con GUI usando Tkinter.**


## Objetivo del juego

Completar el tablero de Kakuro ingresando números del 1 al 9 en las casillas vacías. La suma de los números en una fila o columna debe coincidir con el valor indicado, sin repetir números en ese bloque.


##  Funcionalidades

- Interfaz gráfica con Tkinter
- Múltiples niveles de dificultad (4)
- Partidas aleatorias cargadas desde archivo JSON (3 partidas por nivel)
- Validación automática de jugadas
- Registro de nombre de usuario y estadísticas
- Récords locales
- Soporte para deshacer acciones y rehacer acciones
- Soporte para guardar y cargar partidas


## Estructura del proyecto
 ``` 
programa_3/
│
├── src/
│   └── partidas/
|             └── kakuro2025_facil.json
|             └── kakuro2025_medio.json
|             └── kakuro2025_dificil.json
|             └── kakuro2025_experto.json
|
│   ├── juego.py # Juego principal
│   ├── menus.py # Menús
│   ├── game_logic.py # Reglas y mecánicas del Kakuro
│   ├── kakuro2025_configuracion.json # Configuración
│   ├── kakuro2025_juegoactual.json # Guarda los juegos de los usuarios
│   ├── kakuro2025_records.json # Guarda los récords de todos los usuarios
|
├── documentacion/
│   └── kakuro_manual_de_usuarios.pdf
│   └── kakuro_documentacion_del_proyecto.pdf
|
├── modulos/
│   └── errores.py
├── .gitignore
└── README.md
```

## Ejecución

1. Instalar Python
2. Correr el siguiente comando en la terminal:


```bash
python src/main.py
