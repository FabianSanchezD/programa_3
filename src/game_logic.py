import tkinter as tk #para hacer gui
import json #para leer y hacer jsons
import os #para leer modulos
import sys #para leer modulos x2
import time #para medir tiempo
from datetime import datetime #para tiempo x2
from random import choice #para hacer selecciones aleatorias de partidas
from tkinter import messagebox #para mostrar info al usuario

#añadimos la ruta del proyecto para poder importar módulos correctamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

configs = {} #configs del juego
juego = {} #juego actual
tablero = []  #tablero del juego actual
entries_matrix = [] #esto nos va a servir para guardar las entradas de cada casilla
stack_acciones = []  #stack para guardar las acciones realizadas
stack_para_rehacer = []  #stack para rehacer acciones
botones = []  #almacena los botones de números como canvas
game_window = None  #es la ventana del juego, cerrar o destruir
records = {} #records de todos los juegos
win_callback = None  #callback para cuando se gana el juego
nombre_jugador = "" 
tiempo_inicio = None  #inicio del juego (funciona aparte del temporzador en juego.py)


config_path = os.path.join(os.path.dirname(__file__), "kakuro2025_configuracion.json")

with open(config_path, "r") as file:
    configs = json.load(file)

num_seleccionado = -1  #-1 significa que no se ha seleccionado ningún botón


def resetear_juego():
    """Resetea casi todas las variables globales del juego"""
    global entries_matrix, stack_acciones, stack_para_rehacer, botones, num_seleccionado, game_window, win_callback, nombre_jugador, tiempo_inicio, tablero
    entries_matrix = []
    stack_acciones = []
    stack_para_rehacer = []
    botones = []
    tablero = []
    num_seleccionado = -1  
    win_callback = None
    # Mantener nombre_jugador y tiempo_inicio para que el juego continue

def borrar_partida_actual():
    """Borra solo las entradas del usuario, mantiene la misma partida"""
    global stack_acciones, stack_para_rehacer, num_seleccionado
    
    #limpia todas las entradas del tablero
    for fila in entries_matrix:
        for entry in fila:
            if entry is not None:  #solo si es casilla jugable
                entry.delete(0, tk.END)
    
    stack_acciones = []
    stack_para_rehacer = []
    num_seleccionado = -1

def resetear_total():
    """Resetea todas las variables globales del juego"""
    global entries_matrix, stack_acciones, stack_para_rehacer, botones, num_seleccionado, juego, game_window, win_callback, nombre_jugador, tiempo_inicio, tablero
    entries_matrix = []
    stack_acciones = []
    stack_para_rehacer = []
    botones = []
    juego = {}
    tablero = []
    num_seleccionado = -1  # No hay botón seleccionado
    game_window = None
    win_callback = None
    nombre_jugador = ""
    tiempo_inicio = None

def establecer_botones(botones_arr):
    '''Establece los botones de números del juego'''
    global botones
    botones = botones_arr

def establecer_num_seleccionado(num):
    '''Establece el seleccionado'''
    global num_seleccionado
    num_seleccionado = num

def establecer_win_callback(callback, nombre):
    """Establece la función callback que se ejecutará cuando se gane el juego"""
    global win_callback, nombre_jugador, tiempo_inicio
    nombre_jugador = nombre
    tiempo_inicio = time.time() #inicia el cronometro
    win_callback = callback

def formatear_tiempo(segundos):
    """Convierte segundos a formato hh:mm:ss"""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos = int(segundos % 60)

    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def guardar_record():
    """Guarda el récord del juego actual"""
    global records, nombre_jugador, tiempo_inicio, configs
    
    if tiempo_inicio is None:
        return
    
    tiempo_final = time.time()
    tiempo_transcurrido = tiempo_final - tiempo_inicio - 2
    tiempo_formateado = formatear_tiempo(tiempo_transcurrido)
    
    #fecha
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    
    #dificultad
    nivel = configs.get('nivel', 'facil')

    nuevo_record = {
        "nombre": nombre_jugador,
        "tiempo": tiempo_formateado,
        "fecha": fecha_actual
    }

    if nivel not in records:
        records[nivel] = []
    
    records[nivel].append(nuevo_record)
    
    records[nivel].sort(key=lambda x: x["tiempo"])
    
    records_path = os.path.join(os.path.dirname(__file__), "kakuro2025_records.json")

    with open(records_path, "w") as file:
        json.dump(records, file, indent=4)
    print(f"Récord guardado: {nuevo_record}")

def obtener_clave_fila(fila, columna):
    """Obtiene la clave numérica horizontal para una casilla dada"""
    # Solo buscar hacia la izquierda hasta encontrar la casilla con clave horizontal
    # En Kakuro, la clave SIEMPRE está al inicio del grupo, nunca al final
    for j in range(columna - 1, -1, -1):
        valor = tablero[fila][j]
        
        # Si es una casilla jugable (valor numérico), continuar buscando
        if isinstance(valor, int):
            continue
            
        # Si es una lista (casilla con claves), verificar si tiene clave horizontal
        if isinstance(valor, list):
            if len(valor) >= 2 and valor[1] != 0:  # índice 1 = clave horizontal (F)
                return valor[1]  # Clave horizontal
            # Si no tiene clave horizontal pero es barrera, detener búsqueda
            else:
                break
        # Si es lista vacía, es barrera sin claves
        elif valor == []:
            break
    
    return None

#todas estas funciones que vienen son para validar que el usuario haga un movimiento válido

def obtener_clave_columna(fila, columna):
    """Obtiene la clave numérica vertical para una casilla dada"""
    
    for i in range(fila - 1, -1, -1):
        valor = tablero[i][columna]
        
        if isinstance(valor, int):
            continue
            
        #si es una lista (casilla con claves), verificar si tiene clave vertical
        if isinstance(valor, list):
            if len(valor) >= 2 and valor[0] != 0: 
                return valor[0] 
            else:
                break
        elif valor == []:
            break
    
    return None

def calcular_suma_fila(fila, columna, incluir_nuevo_numero=0):
    """Calcula la suma actual de números en la fila hasta encontrar una barrera (es decir, una casilla no jugable)"""
    suma = incluir_nuevo_numero
    
    #tenemos que buscar a los dos lados
    for j in range(columna - 1, -1, -1):
        valor = tablero[fila][j]
        if isinstance(valor, list) or valor == []:
            break #este break significa que hay una no jugable
        elif valor > 0:
            suma += valor
    
    for j in range(columna + 1, len(tablero[fila])):
        valor = tablero[fila][j]
        if isinstance(valor, list) or valor == []:
            break 
        elif valor > 0:
            suma += valor
    
    return suma

def calcular_suma_columna(fila, columna, incluir_nuevo_numero=0):
    """Calcula la suma actual de números en la columna hasta encontrar una barrera, lo mismo que el de fila eo con columna"""
    suma = incluir_nuevo_numero
    
    #tenemos que buscar a arriba y abajo
    for i in range(fila - 1, -1, -1):
        valor = tablero[i][columna]
        if isinstance(valor, list) or valor == []:
            break #este break significa que hay una no jugable
        elif valor > 0:
            suma += valor

    for i in range(fila + 1, len(tablero)):
        valor = tablero[i][columna]
        if isinstance(valor, list) or valor == []:
            break 
        elif valor > 0:
            suma += valor
    
    return suma

def contar_casillas_vacias_fila(fila, columna):
    """Cuenta cuántas casillas vacías quedan en la fila (incluyendo la actual)"""
    count = 0
    
    #hay que contar la casilla actual si está vacía
    if tablero[fila][columna] == 0:
        count += 1
    
    #tenemos que buscar a ambos lados
    for j in range(columna - 1, -1, -1):
        valor = tablero[fila][j]
        if isinstance(valor, list) or valor == []:
            break
        elif valor == 0:
            count += 1
    
    for j in range(columna + 1, len(tablero[fila])):
        valor = tablero[fila][j]
        if isinstance(valor, list) or valor == []:
            break
        elif valor == 0:
            count += 1
    
    return count

def contar_casillas_vacias_columna(fila, columna):
    """Cuenta cuántas casillas vacías quedan en la columna (incluyendo la actual), lo mismo que el de fila"""
    count = 0
    
    #hay que contar la casilla actual si está vacía
    if tablero[fila][columna] == 0:
        count += 1
    
    #tenemos que buscar a ambos lados
    for i in range(fila - 1, -1, -1):
        valor = tablero[i][columna]
        if isinstance(valor, list) or valor == []:
            break
        elif valor == 0:
            count += 1
    
    for i in range(fila + 1, len(tablero)):
        valor = tablero[i][columna]
        if isinstance(valor, list) or valor == []:
            break
        elif valor == 0:
            count += 1
    
    return count

def click_num(event, row, col):
    '''Esto es para manejar el click de un num o borrador en el tablero'''
    global num_seleccionado
    if num_seleccionado == -1:  #no se selecciono numero
        messagebox.showwarning("Número no seleccionado", "Por favor, seleccione un número del 1 al 9 o el borrador antes de hacer clic en el tablero.")
        return
    elif num_seleccionado == 0:
        #actualizar el tablero al borrar
        if tablero[row][col] != 0:
            tablero[row][col] = 0
        event.widget.delete(0, tk.END)
        return
    else:
        #tenemos que validar que no hayan más nums iguales en las filas
        numeros_en_grupo_fila = []

        #tenemos que buscar a ambos lados
        for j in range(col - 1, -1, -1):
            valor = tablero[row][j]
            if isinstance(valor, list) or valor == []:
                break
            elif valor > 0:
                numeros_en_grupo_fila.append(valor)

        for j in range(col + 1, len(tablero[row])):
            valor = tablero[row][j]
            if isinstance(valor, list) or valor == []:
                break
            elif valor > 0:
                numeros_en_grupo_fila.append(valor)
        
        if num_seleccionado in numeros_en_grupo_fila:
            messagebox.showwarning("Número repetido", f"El número {num_seleccionado} ya está en este grupo de la fila.")
            return
        
        #tenemos que validar que no hayan más nums iguales en las columnas
        numeros_en_grupo_columna = []

        #tenemos que buscar a ambos lados
        for i in range(row - 1, -1, -1):
            valor = tablero[i][col]
            if isinstance(valor, list) or valor == []:
                break
            elif valor > 0:
                numeros_en_grupo_columna.append(valor)

        for i in range(row + 1, len(tablero)):
            valor = tablero[i][col]
            if isinstance(valor, list) or valor == []:
                break
            elif valor > 0:
                numeros_en_grupo_columna.append(valor)
        
        if num_seleccionado in numeros_en_grupo_columna:
            messagebox.showwarning("Número repetido", f"El número {num_seleccionado} ya está en este grupo de la columna.")
            return
        
        #ahora validemos la suma de fila
        clave_fila = obtener_clave_fila(row, col)
        if clave_fila:
            suma_actual_fila = calcular_suma_fila(row, col, num_seleccionado)
            casillas_vacias_fila = contar_casillas_vacias_fila(row, col)
            
            #si la suma es mayor a la clave
            if suma_actual_fila > clave_fila:
                messagebox.showwarning("Suma excedida", f"JUGADA NO ES VÁLIDA PORQUE LA SUMA DE LA FILA SERÍA {suma_actual_fila} Y LA CLAVE NUMÉRICA ES {clave_fila}")
                return
            #solo queda esa casilla y no coincide
            elif casillas_vacias_fila == 1 and suma_actual_fila != clave_fila:
                messagebox.showwarning("Suma inválida", f"JUGADA NO ES VÁLIDA PORQUE LA SUMA DE LA FILA SERÍA {suma_actual_fila} INCLUIDA LA CASILLA Y LA CLAVE NUMÉRICA ES {clave_fila}")
                return
        
        #ahora validemos la suma de columna
        clave_columna = obtener_clave_columna(row, col)
        if clave_columna:
            suma_actual_columna = calcular_suma_columna(row, col, num_seleccionado)
            casillas_vacias_columna = contar_casillas_vacias_columna(row, col)
            
            #si la suma es mayor a la clave
            if suma_actual_columna > clave_columna:
                messagebox.showwarning("Suma excedida", f"JUGADA NO ES VÁLIDA PORQUE LA SUMA DE LA COLUMNA SERÍA {suma_actual_columna} Y LA CLAVE NUMÉRICA ES {clave_columna}")
                return
            #solo queda esa casilla y no coincide
            elif casillas_vacias_columna == 1 and suma_actual_columna != clave_columna:
                messagebox.showwarning("Suma inválida", f"JUGADA NO ES VÁLIDA PORQUE LA SUMA DE LA COLUMNA SERÍA {suma_actual_columna} INCLUIDA LA CASILLA Y LA CLAVE NUMÉRICA ES {clave_columna}")
                return
        else:
            pass
        
        #esto significa que la jugada es válida
        event.widget.delete(0, tk.END)
        event.widget.insert(0, str(num_seleccionado))
        tablero[row][col] = num_seleccionado
        print(tablero)
        continuar = False
        for i in range(len(tablero)):
            for j in range(len(tablero[i])):
                if tablero[i][j] == 0:
                    continuar = True
                    break

        print(continuar)
        if not continuar:
            #esto significa que ganó
            guardar_record()
            messagebox.showinfo("¡Felicidades!", "Terminó el juego exitosamente.")
            if game_window:
                game_window.destroy()
            resetear_total()
            if win_callback:
                win_callback()

        stack_acciones.append((row + 1, col + 1, num_seleccionado)) #guarda la ultima accion en la pila

def crear_casilla(canvas, cord_x, cord_y, fila, columna, suma_ver=None, suma_hor=None, jugable=False):
    '''Esta función es del grupo para crear el tablero visual del juego, es para hacer las casillas'''

    #lo que hacemos es encontrar si tiene suma vertical u horizontal, si no tiene ninguna, es jugable
    # si tiene alguna, no es jugable
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
        entry.bind("<KeyPress>", lambda event: validar_teclado_bloqueado(event))
        
        return entry

    if suma_ver:
        canvas.create_text(cord_x + 38, cord_y + 7, text=f"{suma_ver}", font=("Arial", 8), anchor="ne")
    if suma_hor:
        canvas.create_text(cord_x + 7, cord_y + 38, text=f"{suma_hor}", font=("Arial", 8), anchor="sw")
    return None

def crear_tablero(tamano, datos):
    '''Crea un tablero a partir del cual se va a jugar, es como una matriz'''
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
            tablero[num_fila][num_columna] = [] #no jugable
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
    '''Creamos el tablero visual que se va a mostrar al usuario'''
    global entries_matrix
    
    #hacemos la matriz entries_matriz
    entries_matrix = [[None for _ in range(tamano)] for _ in range(tamano)] #esta parte fue tomada de una ia, ver documentacion
    
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
                    crear_casilla(canvas, cord_x, cord_y, i, j, jugable=False) #esta era la funcion pasada
                else:
                    suma_hor = valor_celda[0] if valor_celda[0] != 0 else None  
                    suma_ver = valor_celda[1] if valor_celda[1] != 0 else None  
                    crear_casilla(canvas, cord_x, cord_y, i, j, suma_ver=suma_ver, suma_hor=suma_hor)
    
    return canvas

exclude = []
def cargar_partida(nivel, cambiar_partida=True, juego_window=None):
    '''Con esta lo que hacemos es cargar una partida de la dificultad correcta y aleatoria del json'''
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

    else:
        if juego and len(juego) > 0:
            #si hay partida, mantenerla
            partida_seleccionada = juego[0]

        else:
            #si no hay partida, cargar
            if len(exclude) >= len(juegos):
                exclude = []
            decision = choice(list(set(range(len(juegos))) - set(exclude)))
            exclude.append(decision)
            partida_seleccionada = juegos[decision]
            print(f"Primera partida cargada: {partida_seleccionada['partida']}")

    return [partida_seleccionada]


def setup_juego(root, tamano=9, cambiar_partida=True, usar_tablero_cargado=False):
    '''Con esta función hacemos el setup del juego, agarramos configs, records, partidas y creamos tableros'''
    global records
    global botones
    global configs, juego, tablero, game_window

    # Almacenar referencia a la ventana del juego
    game_window = root

    config_path = os.path.join(os.path.dirname(__file__), "kakuro2025_configuracion.json")

    with open(config_path, "r") as file:
        configs = json.load(file)

    records_path = os.path.join(os.path.dirname(__file__), "kakuro2025_records.json")

    with open(records_path, "r") as file:
        records = json.load(file)

    print(records)
    nivel = configs['nivel']
    
    # Si no usamos tablero cargado, cargar una nueva partida
    if not usar_tablero_cargado:
        juego = cargar_partida(nivel, cambiar_partida, root)
        
        # Si no hay partidas disponibles, cargar_partida retorna None
        if juego is None:
            return None
        
        tablerov = crear_tablero(tamano, juego)
    else:
        # Usar el tablero ya cargado en la variable global
        tablerov = tablero
    
    tablerof = crear_tablero_final(root, tamano, tablerov)

    return tablerof


def deshacer_jugada():
    '''Esta función es para deshacer jugadas, sirve para el boton de deshacer que esta en el juego.py'''
    global stack_acciones, stack_para_rehacer
    if not stack_acciones:
        return

    ultima = stack_acciones.pop()
    stack_para_rehacer.append(ultima)  #guarda la acción para deshacerla
    fila = ultima[0]
    columna = ultima[1]
    entry = entries_matrix[fila - 1][columna - 1]

    if entry:
        entry.delete(0, tk.END)
        tablero[fila - 1][columna - 1] = 0
        print(f"Deshecha jugada: {ultima}")
        print(f"Stack acciones: {stack_acciones}")

def rehacer_jugada():
    '''Esta función es para rehacer jugadas, sirve para el boton de rehacer que esta en el juego.py'''
    global stack_acciones, stack_para_rehacer
    if not stack_para_rehacer:
        return

    ultima = stack_para_rehacer.pop()
    stack_acciones.append(ultima)  #agrega otra vez al stack de acciones
    fila = ultima[0]
    columna = ultima[1]
    num = ultima[2]
    entry = entries_matrix[fila - 1][columna - 1]

    if entry:
        entry.delete(0, tk.END)
        entry.insert(0, str(num))
        tablero[fila - 1][columna - 1] = num
        print(f"Rehecha jugada: {ultima}")
        print(f"Stack para rehacer: {stack_para_rehacer}")

def validar_teclado_bloqueado(event):
    """Controla la entrada de teclado según el número seleccionado, también para poder usar numeros en lugar de los botones"""
    global num_seleccionado
    if num_seleccionado == -1:
        messagebox.showwarning("Número no seleccionado", "Por favor, seleccione un número del 1 al 9 o el borrador antes de escribir en el tablero.")
        return "break" #no deja
    elif num_seleccionado == 0:
        if event.keysym in ['Delete', 'BackSpace']:
            return None
        else:
            return "break"
    else:
        if event.char == str(num_seleccionado) or event.keysym in ['Delete', 'BackSpace']:
            return None 
        else:
            return "break"


def obtener_estado_juego():
    """Consigue el estado del juego actualmente"""
    global tablero, stack_acciones, configs, nombre_jugador
    
    #vuelve todo un diccionario que podemos guardar en el json
    stack_como_listas = []
    for accion in stack_acciones:
        if isinstance(accion, tuple):
            stack_como_listas.append(list(accion))
        elif isinstance(accion, list):
            stack_como_listas.append(accion)
        else:
            stack_como_listas.append(accion)
    
    return {
        "nombre_jugador": nombre_jugador,
        "tablero": tablero,
        "stack_acciones": stack_como_listas,
        "nivel": configs.get('nivel', 'facil'),
        "fecha_guardado": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

def cargar_estado_juego(estado):
    """Carga un estado de juego guardado y actualiza el tablero visual"""
    global tablero, stack_acciones, nombre_jugador
    
    if estado:
        tablero_guardado = estado.get("tablero", []) #si tablero no tiene nada, ponemos una lista vacía 
    
        tablero = []
        for i in range(len(tablero_guardado)):
            fila = []
            for j in range(len(tablero_guardado[i])):
                valor = tablero_guardado[i][j]
                if isinstance(valor, int):
                    fila.append(0)
                else:
                    fila.append(valor)
            tablero.append(fila)
        
        #vuelve las acciones a tuplas
        stack_guardado = estado.get("stack_acciones", [])
        stack_acciones = []
        for accion in stack_guardado:
            if isinstance(accion, list) and len(accion) >= 3:
                stack_acciones.append(tuple(accion))
            else:
                stack_acciones.append(accion)
        
        nombre_jugador = estado.get("nombre_jugador", "")
        
        #actualiza entradas del tablero visual
        if entries_matrix:
            for i in range(len(tablero_guardado)):
                for j in range(len(tablero_guardado[i])):
                    if entries_matrix[i][j] is not None: #jugable
                        entries_matrix[i][j].delete(0, tk.END)
                        valor_guardado = tablero_guardado[i][j]

                        if isinstance(valor_guardado, int) and valor_guardado > 0:
                            entries_matrix[i][j].insert(0, str(valor_guardado))
        