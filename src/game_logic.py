import tkinter as tk
import json
import os

configs = {}
juego = {}

config_path = os.path.join(os.path.dirname(__file__), "kakuro2025_configuracion.json")

with open(config_path, "r") as file:
    configs = json.load(file)


def crear_casilla(canvas, cord_x, cord_y, suma_ver=None, suma_hor=None, jugable=False): #arreglar lo de jugable
    if suma_ver or suma_hor or not jugable:      
        canvas.create_rectangle(cord_x, cord_y, cord_x + 45, cord_y + 45, fill="gray", outline="black")
    elif jugable:
        canvas.create_rectangle(cord_x, cord_y, cord_x + 45, cord_y + 45, fill="white", outline="black")
        # Create entry widget for playable cells
        entry = tk.Entry(canvas, width=2, font=('Arial', 12), justify='center')
        canvas.create_window(cord_x + 22, cord_y + 22, window=entry)

    if suma_ver or suma_hor or not jugable:
        canvas.create_line(cord_x, cord_y, cord_x + 45, cord_y + 45, fill="black")

    if suma_ver:
        canvas.create_text(cord_x + 7, cord_y + 38, text=f"{suma_ver}", font=("Arial", 8), anchor="sw")
    if suma_hor:
        canvas.create_text(cord_x + 38, cord_y + 7, text=f"{suma_hor}", font=("Arial", 8), anchor="ne")

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
    
    return tablero

def crear_tablero_final(root, tamano, tablero):
    canvas = tk.Canvas(root, width=tamano*45 + 10, height=tamano*45 + 10, bg="white")
    canvas.grid(row=1, column=0, columnspan=6, padx=10, pady=10)
    
    for i in range(tamano):
        for j in range(tamano):
            cord_x = j * 45 + 5
            cord_y = i * 45 + 5
            
            valor_celda = tablero[i][j]
            
            if valor_celda == 0:
                crear_casilla(canvas, cord_x, cord_y, jugable=True)
            elif isinstance(valor_celda, list):
                if not valor_celda:
                    crear_casilla(canvas, cord_x, cord_y, jugable=False)
                else:
                    suma_hor = valor_celda[0] if valor_celda[0] != 0 else None
                    suma_ver = valor_celda[1] if valor_celda[1] != 0 else None
                    crear_casilla(canvas, cord_x, cord_y, suma_ver=suma_ver, suma_hor=suma_hor)
    
    return canvas

def cargar_partida(nivel):
    archivo = f"kakuro2025_{nivel}.json"
    ruta = os.path.join(os.path.dirname(__file__), "partidas", archivo)
        
    with open(ruta, "r") as file:
        juego = json.load(file)
    
    return juego


def setup_juego(root, tamano=9):
    global configs, juego, tablero

    nivel = configs['nivel']
    
    juego = cargar_partida(nivel)
    
    tablerov = crear_tablero(tamano, juego)
    
    tablerof = crear_tablero_final(root, tamano, tablerov)
    
    return tablerof
