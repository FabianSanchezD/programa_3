import tkinter as tk
import json
import os
import sys
from random import choice
from tkinter import messagebox

# Añade la ruta del proyecto para poder importar módulos correctamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

configs = {}
juego = {}
entries_matrix = [] #esto nos va a servir para guardar las entradas de cada casilla, para también luego borrarlas o modificarlas
stack_acciones = []  # Pila para guardar las acciones realizadas
botones = []  # Almacenará los botones de números


config_path = os.path.join(os.path.dirname(__file__), "kakuro2025_configuracion.json")

with open(config_path, "r") as file:
    configs = json.load(file)

num_seleccionado = 0


def resetear_juego():
    """Resetea todas las variables globales del juego"""
    global entries_matrix, stack_acciones, stack_para_rehacer, botones, num_seleccionado
    entries_matrix = []
    stack_acciones = []
    stack_para_rehacer = []
    botones = []
    num_seleccionado = 0
    print("Variables del juego reseteadas")

def borrar_partida_actual():
    """Borra solo las entradas del usuario, mantiene la misma partida"""
    global stack_acciones, stack_para_rehacer, num_seleccionado
    
    # Limpiar todas las entradas del tablero
    for fila in entries_matrix:
        for entry in fila:
            if entry is not None:  # Solo si es una casilla jugable
                entry.delete(0, tk.END)
    
    # Limpiar los stacks de acciones
    stack_acciones = []
    stack_para_rehacer = []
    num_seleccionado = 0
    print("Partida actual borrada - misma partida, tablero limpio")

def resetear_total():
    """Resetea todas las variables globales del juego"""
    global entries_matrix, stack_acciones, stack_para_rehacer, botones, num_seleccionado, juego
    entries_matrix = []
    stack_acciones = []
    stack_para_rehacer = []
    botones = []
    juego = {}
    num_seleccionado = 0
    print("Variables del juego reseteadas totalmente")

def establecer_botones(botones_arr):
    global botones
    botones = botones_arr
    print(f"Botones establecidos en game_logic: {botones}")

def establecer_num_seleccionado(num):
    global num_seleccionado
    num_seleccionado = num
    print(f"seleccionado: {num_seleccionado}")

def click_num(event, row, col):
    global num_seleccionado
    if num_seleccionado == 0:  #0 es borrador
        event.widget.delete(0, tk.END)
    else:
        event.widget.delete(0, tk.END)
        event.widget.insert(0, str(num_seleccionado))
        stack_acciones.append((row + 1, col + 1, num_seleccionado)) #guarda la ultima accion en la pila
        print(stack_acciones)

def crear_casilla(canvas, cord_x, cord_y, fila, columna, suma_ver=None, suma_hor=None, jugable=False):
    global entries_matrix
    if suma_ver or suma_hor or not jugable:      
        canvas.create_rectangle(cord_x, cord_y, cord_x + 45, cord_y + 45, fill="gray", outline="black")
        
    if suma_ver or suma_hor:
        canvas.create_line(cord_x, cord_y, cord_x + 45, cord_y + 45, fill="black")
        
    elif jugable:
        canvas.create_rectangle(cord_x, cord_y, cord_x + 45, cord_y + 45, fill="white", outline="black")
        entry = tk.Entry(canvas, width=2, font=('Arial', 12), justify='center')
        canvas.create_window(cord_x + 22, cord_y + 22, window=entry)
        
        entry.bind("<Button-1>", lambda event, r=fila, c=columna: click_num(event, r, c))
        
        return entry

    if suma_ver:
        canvas.create_text(cord_x + 38, cord_y + 7, text=f"{suma_ver}", font=("Arial", 8), anchor="ne")
    if suma_hor:
        canvas.create_text(cord_x + 7, cord_y + 38, text=f"{suma_hor}", font=("Arial", 8), anchor="sw")
    return None

def crear_tablero(tamano, datos):
    global tablero
    tablero = []
    for i in range(tamano):
        fila = []
        for j in range(tamano):
            fila.append(0) #si queda solo 0, significa que es casilla vacia jugable

        tablero.append(fila)

    for dato in datos[0]["claves"]:
        num_fila = dato["fila"] - 1
        num_columna = dato["columna"] - 1
        
        if dato["clave"] == 0:
            tablero[num_fila][num_columna] = []  #no jugable
            continue

        if isinstance(tablero[num_fila][num_columna], list):
            if dato["tipo_de_clave"] == "C":
                tablero[num_fila][num_columna][0] = dato["clave"]
            else:  
                tablero[num_fila][num_columna][1] = dato["clave"]
        else:
            if dato["tipo_de_clave"] == "C":
                tablero[num_fila][num_columna] = [dato["clave"], 0]
            else:
                tablero[num_fila][num_columna] = [0, dato["clave"]]
    print(tablero)
    return tablero

def crear_tablero_final(root, tamano, tablero):
    global entries_matrix
    
    # Inicializar matriz de entries
    entries_matrix = [[None for _ in range(tamano)] for _ in range(tamano)] # revisar esto
    
    canvas = tk.Canvas(root, width=tamano*45 + 10, height=tamano*45 + 10, bg="white")
    canvas.grid(row=1, column=0, columnspan=6, padx=10, pady=10)
    
    for i in range(tamano):
        for j in range(tamano):
            cord_x = j * 45 + 5
            cord_y = i * 45 + 5
            
            valor_celda = tablero[i][j]
            
            if valor_celda == 0:
                entry = crear_casilla(canvas, cord_x, cord_y, i, j, jugable=True)
                entries_matrix[i][j] = entry

            else:
                if valor_celda == []:
                    crear_casilla(canvas, cord_x, cord_y, i, j, jugable=False)
                else:
                    suma_hor = valor_celda[0] if valor_celda[0] != 0 else None  
                    suma_ver = valor_celda[1] if valor_celda[1] != 0 else None  
                    print(f"creando casilla con {suma_ver} y {suma_hor}")
                    crear_casilla(canvas, cord_x, cord_y, i, j, suma_ver=suma_ver, suma_hor=suma_hor)
    
    return canvas

exclude = []
def cargar_partida(nivel, cambiar_partida=True, juego_window=None):
    global exclude, juego
    archivo = f"kakuro2025_{nivel}.json"
    ruta = os.path.join(os.path.dirname(__file__), "partidas", archivo)
        
    with open(ruta, "r") as file:
        juegos = json.load(file)

    if juegos == []:
        messagebox.showerror("Error", "No hay partidas disponibles para este nivel, lo lamentamos.")
        if juego_window:
            juego_window.destroy()
        return None

    if cambiar_partida:
        if len(exclude) >= len(juegos):
            exclude = []

        decision = choice(list(set(range(len(juegos))) - set(exclude)))
        exclude.append(decision)
        partida_seleccionada = juegos[decision]
        print(f"Nueva partida cargada: {partida_seleccionada['partida']}")
    else:
        # Mantener la partida actual si existe
        if juego and len(juego) > 0:
            partida_seleccionada = juego[0]
            print(f"Manteniendo partida actual: {partida_seleccionada['partida']}")
        else:
            # Si no hay partida actual, cargar una nueva
            if len(exclude) >= len(juegos):
                exclude = []
            decision = choice(list(set(range(len(juegos))) - set(exclude)))
            exclude.append(decision)
            partida_seleccionada = juegos[decision]
            print(f"Primera partida cargada: {partida_seleccionada['partida']}")

    return [partida_seleccionada]


def setup_juego(root, tamano=9, cambiar_partida=True):
    global botones
    global configs, juego, tablero

    config_path = os.path.join(os.path.dirname(__file__), "kakuro2025_configuracion.json")

    with open(config_path, "r") as file:
        configs = json.load(file)

    nivel = configs['nivel']
    
    juego = cargar_partida(nivel, cambiar_partida, root)
    
    # Si no hay partidas disponibles, cargar_partida retorna None
    if juego is None:
        return None
    
    tablerov = crear_tablero(tamano, juego)
    
    tablerof = crear_tablero_final(root, tamano, tablerov)

    return tablerof


stack_para_rehacer = []

def deshacer_jugada():
    global stack_acciones, stack_para_rehacer
    if not stack_acciones:
        print("No hay jugadas para deshacer")
        return

    ultima = stack_acciones.pop()
    stack_para_rehacer.append(ultima)  # Guarda la acción deshecha para rehacerla
    fila = ultima[0]
    columna = ultima[1]
    entry = entries_matrix[fila - 1][columna - 1]

    if entry:
        entry.delete(0, tk.END)
        print(f"Deshecha jugada: {ultima}")
        print(f"Stack acciones: {stack_acciones}")

def rehacer_jugada():
    global stack_acciones, stack_para_rehacer
    if not stack_para_rehacer:
        print("No hay jugadas para rehacer")
        return

    ultima = stack_para_rehacer.pop()
    stack_acciones.append(ultima)  # Vuelve a agregar la acción al stack principal
    fila = ultima[0]
    columna = ultima[1]
    num = ultima[2]
    entry = entries_matrix[fila - 1][columna - 1]

    if entry:
        entry.delete(0, tk.END)
        entry.insert(0, str(num))
        print(f"Rehecha jugada: {ultima}")
        print(f"Stack para rehacer: {stack_para_rehacer}")