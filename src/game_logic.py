import tkinter as tk
import json
import os

configs = {}
juego = {}
entries_matrix = [] #esto nos va a servir para guardar las entradas de cada casilla, para también luego borrarlas o modificarlas
stack_acciones = []  # Pila para guardar las acciones realizadas

config_path = os.path.join(os.path.dirname(__file__), "kakuro2025_configuracion.json")

with open(config_path, "r") as file:
    configs = json.load(file)

num_seleccionado = 0

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
        stack_acciones.append((row, column, num_seleccionado)) #guarda la ultima accion en la pila

def crear_casilla(canvas, cord_x, cord_y, fila, columna, suma_ver=None, suma_hor=None, jugable=False):
    global entries_matrix
    if suma_ver or suma_hor or not jugable:      
        canvas.create_rectangle(cord_x, cord_y, cord_x + 45, cord_y + 45, fill="gray", outline="black")
        return None
    elif jugable:
        canvas.create_rectangle(cord_x, cord_y, cord_x + 45, cord_y + 45, fill="white", outline="black")
        entry = tk.Entry(canvas, width=2, font=('Arial', 12), justify='center')
        canvas.create_window(cord_x + 22, cord_y + 22, window=entry)
        
        entry.bind("<Button-1>", lambda event, r=fila, c=columna: click_num(event, r, c))
        
        return entry

    if suma_ver or suma_hor or not jugable:
        canvas.create_line(cord_x, cord_y, cord_x + 45, cord_y + 45, fill="black")

    if suma_ver:
        canvas.create_text(cord_x + 7, cord_y + 38, text=f"{suma_ver}", font=("Arial", 8), anchor="sw")
    if suma_hor:
        canvas.create_text(cord_x + 38, cord_y + 7, text=f"{suma_hor}", font=("Arial", 8), anchor="ne")
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

            elif isinstance(valor_celda, list):
                if not valor_celda:
                    crear_casilla(canvas, cord_x, cord_y, i, j, jugable=False)
                else:
                    suma_hor = valor_celda[0] if valor_celda[0] != 0 else None
                    suma_ver = valor_celda[1] if valor_celda[1] != 0 else None
                    crear_casilla(canvas, cord_x, cord_y, i, j, suma_ver=suma_ver, suma_hor=suma_hor)
    
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
