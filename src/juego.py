'''
Instituto Tecnológico de Costa Rica

Programa #3: Kakuro

Fabián Sánchez Durán

Profesor: William Mata Rodríguez

I Semestre 2025
'''

import os #más que todo para paths a archivos
import json #para cargar o escribir jsons
import sys #para añadir el directorio del proyecto al path y poder importar módulos correctamente
from tkinter import messagebox #para poner mensajes en pantalla

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modulos import errores #para errores (solo se usó 1 vez)
from src import game_logic #logica del juego
from src import menus #menus del juego
import tkinter as tk #para hacer el gui


borrado = False
terminado = False
guardados = []

def main():
    """Función principal del programa, inicia el juego y muestra las ventanas principales. De aquí deriva todo lo demás"""
 
    script_dir = os.path.dirname(os.path.abspath(__file__))

    
    def iniciar_juego():
        """Con esta función iniciamos el juego, primero va a pedir un nombre"""
        antes_jugar = tk.Toplevel()
        antes_jugar.title("Kakuro - Antes de Jugar")
        antes_jugar.geometry("360x250")

        info = tk.Label(antes_jugar, text="Antes de jugar, ¿cuál es su nombre?", font=("Futura", 14))
        info.grid(row=0, column=0, padx=20, pady=20)

        nombre_entry = tk.Entry(antes_jugar, font=("Futura", 12))
        nombre_entry.grid(row=1, column=0, padx=20, pady=10)

        continuar = tk.Button(antes_jugar, text="Continuar", font=("Futura", 12), command=lambda: iniciar_partida(nombre_entry.get()))
        continuar.grid(row=2, column=0, padx=20, pady=10)
    
        def mostrar_overlay_iniciar(ventana_juego):
            """Crea y muestra el overlay de iniciar juego, esto es una forma de hacer el botón iniciar juego para hacerlo más visible"""
            overlay = tk.Toplevel(ventana_juego)
            overlay.title("Kakuro - Jugando")
            
            def cerrar_overlay_e_iniciar_reloj():
                '''Cierra el boton de iniciar juego y comienza a correr el reloj'''
                overlay.destroy()
                ventana_juego.iniciar_reloj() #esta función inicia el reloj, ver más adelante
            
            tk.Button(overlay, text="INICIAR JUEGO", font=("Futura",20), bg='green', 
                     command=cerrar_overlay_e_iniciar_reloj).pack(pady=400)
            overlay.grab_set() 
            overlay.transient(ventana_juego)
            
            ventana_juego.update_idletasks()
            
            juego_x = ventana_juego.winfo_x()
            juego_y = ventana_juego.winfo_y()
            juego_width = ventana_juego.winfo_width()
            juego_height = ventana_juego.winfo_height()

            overlay_width = 600
            overlay_height = 900
            overlay.geometry(f"{overlay_width}x{overlay_height}+{juego_x + (juego_width - overlay_width)//2}+{juego_y + (juego_height - overlay_height)//2}")
            
            return overlay

        def borrar_juego(window, nombre):
            '''Esto servirá para el botón de borrar el juego, pero dejar la misma partida'''
            respuesta = messagebox.askyesno("Borrar Juego", "¿Está seguro de que desea borrar el juego actual?\n(Se mantendrá la misma partida)")
            if respuesta:
                game_logic.borrar_partida_actual() #esta función borra las entradas del usuario y el stack de acciones pero no el tablero

                window.reiniciar_reloj()
                
                mostrar_overlay_iniciar(window)

        def terminar_juego(window, nombre):
            '''Esto sirve como para que el usuario se rinda, es decir, borra la partida completamente e inicia otra'''
            respuesta = messagebox.askyesno("Terminar Juego", "¿Está seguro de que desea terminar el juego?\n(Se cambiará a una nueva partida)")
            if respuesta:
                window.destroy()
                iniciar_partida(nombre)
                terminado = True

        def mostrar_records(game_window=None):
            '''Esta función sirve para el botón de records'''

            def mostrar_records_seleccionados(records, dificultad, jugadores):
                '''Mostramos los records en una ventana nueva'''
                recordstab.destroy() #borramos primero la ventana para seleccionar los records
                
                if dificultad == "todos":
                    records_finales = {}
                    for nivel, records_nivel in records.items():
                        records_finales[nivel] = records_nivel
                else:
                    records_finales = records.get(dificultad, []) #records_finales se vuelve [] si no hay records
                    
                if jugadores == "yo":
                    if dificultad == "todos":
                        #filtrar todos los niveles, para esta parte usé list comprehensions e ia (ver en documentacion)
                        for nivel in records_finales:
                            records_finales[nivel] = [record for record in records_finales[nivel] if record['nombre'] == game_logic.nombre_jugador]
                    else:
                        #filtrar solo el nivel seleccionado
                        records_finales = [record for record in records_finales if record['nombre'] == game_logic.nombre_jugador]
                elif jugadores == "todos_jugadores":
                    pass  #no filtrar+
                
                records_window = tk.Toplevel()
                records_window.title("Kakuro - Récords Seleccionados")
                records_window.geometry("500x640")
                records_window.columnconfigure(0, weight=1)
                records_window.columnconfigure(1, weight=1)
                records_window.columnconfigure(2, weight=1)

                titulo = tk.Label(records_window, text="Récords", font=("Futura", 24, "bold"))
                titulo.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

                row_counter = 1

                if dificultad == "todos":
                    for nivel, records_nivel in records_finales.items():
                        if records_nivel:
                            tk.Label(records_window, text=f"Nivel: {nivel.upper()}", font=("Futura", 16, "bold")).grid(row=row_counter, column=0, columnspan=4, padx=10, pady=(10,5))
                            row_counter += 1
                            
                            #headers
                            tk.Label(records_window, text="JUGADOR", font=("Futura", 12, "bold")).grid(row=row_counter, column=0, padx=5, pady=2)
                            tk.Label(records_window, text="TIEMPO", font=("Futura", 12, "bold")).grid(row=row_counter, column=1, padx=5, pady=2)
                            tk.Label(records_window, text="FECHA", font=("Futura", 12, "bold")).grid(row=row_counter, column=2, padx=5, pady=2)
                            row_counter += 1

                            for i, record in enumerate(records_nivel, 1):
                                tk.Label(records_window, text=f"{i} - {record['nombre']}", font=("Futura", 10)).grid(row=row_counter, column=0, padx=5, pady=1)
                                tk.Label(records_window, text=f"{record['tiempo']}", font=("Futura", 10)).grid(row=row_counter, column=1, padx=5, pady=1)
                                tk.Label(records_window, text=f"{record['fecha']}", font=("Futura", 10)).grid(row=row_counter, column=2, padx=5, pady=1)
                                row_counter += 1
                else:
                    tk.Label(records_window, text=f"Nivel: {dificultad.upper()}", font=("Futura", 16, "bold")).grid(row=row_counter, column=0, columnspan=4, padx=10, pady=(10,5))
                    row_counter += 1
                    
                    #headers
                    tk.Label(records_window, text="JUGADOR", font=("Futura", 12, "bold")).grid(row=row_counter, column=0, padx=5, pady=2)
                    tk.Label(records_window, text="TIEMPO", font=("Futura", 12, "bold")).grid(row=row_counter, column=1, padx=5, pady=2)
                    tk.Label(records_window, text="FECHA", font=("Futura", 12, "bold")).grid(row=row_counter, column=2, padx=5, pady=2)
                    row_counter += 1
                    
                    if records_finales:
                        for i, record in enumerate(records_finales, 1):
                            tk.Label(records_window, text=f"{i} - {record['nombre']}", font=("Futura", 10)).grid(row=row_counter, column=0, padx=5, pady=1)
                            tk.Label(records_window, text=f"{record['tiempo']}", font=("Futura", 10)).grid(row=row_counter, column=1, padx=5, pady=1)
                            tk.Label(records_window, text=f"{record['fecha']}", font=("Futura", 10)).grid(row=row_counter, column=2, padx=5, pady=1)
                            row_counter += 1
                    else:
                        tk.Label(records_window, text="No hay récords para este nivel", font=("Futura", 12)).grid(row=row_counter, column=0, columnspan=3, padx=10, pady=10)

                def on_records_window_closing():
                    '''Esta función sirve que para cuando se cierre la ventana de records, se reanude el reloj del juego si existe'''
                    if game_window and hasattr(game_window, 'iniciar_reloj'):
                        game_window.iniciar_reloj()
                    records_window.destroy()
                
                records_window.protocol("WM_DELETE_WINDOW", on_records_window_closing) #reanuda el reloj al cerrar la ventana de records


            records_path = os.path.join(script_dir, "kakuro2025_records.json")

            with open(records_path, "r") as file:
                records = json.load(file)

            #pausa el reloj si existe
            if game_window and hasattr(game_window, 'pausar_reloj'):
                game_window.pausar_reloj()

            recordstab = tk.Toplevel()
            recordstab.title("Kakuro - Récords")
            recordstab.geometry("400x550")
            
            # Reanudar el reloj cuando se cierre la ventana de récords
            def on_closing():
                '''Misma función que la de arriba, pero para el recordstab'''
                if game_window and hasattr(game_window, 'iniciar_reloj'):
                    game_window.iniciar_reloj()
                recordstab.destroy()
            
            recordstab.protocol("WM_DELETE_WINDOW", on_closing)

            recordstab.columnconfigure(0, weight=1)
            recordstab.columnconfigure(1, weight=1)
            recordstab.columnconfigure(2, weight=1)

            titulo = tk.Label(recordstab, text="Récords", font=("Futura", 24, "bold"))
            titulo.grid(row=0, column=1, columnspan=2, padx=20, pady=20)

            dificultad= tk.StringVar(value="facil")

            dificultad_label = tk.Label(recordstab, text="Dificultad:", font=("Futura", 16, 'bold'))
            dificultad_label.grid(row=1, column=1, columnspan=2, padx=20, pady=10, sticky='w')

            todos_rb = tk.Radiobutton(recordstab, text="Todos los niveles", variable=dificultad, value="todos", font=("Futura", 14))
            todos_rb.grid(row=2, column=1, padx=5, pady=2, sticky='w')
            facil_rb = tk.Radiobutton(recordstab, text="Fácil", variable=dificultad, value="facil", font=("Futura", 14))
            facil_rb.grid(row=3, column=1, padx=5, pady=2, sticky='w')
            medio_rb = tk.Radiobutton(recordstab, text="Medio", variable=dificultad, value="medio", font=("Futura", 14))
            medio_rb.grid(row=4, column=1, padx=5, pady=2, sticky='w')
            dificil_rb = tk.Radiobutton(recordstab, text="Difícil", variable=dificultad, value="dificil", font=("Futura", 14))
            dificil_rb.grid(row=5, column=1, padx=5, pady=2, sticky='w')
            experto_rb = tk.Radiobutton(recordstab, text="Experto", variable=dificultad, value="experto", font=("Futura", 14))
            experto_rb.grid(row=6, column=1, padx=5, pady=2, sticky='w')

            jugadores = tk.StringVar(value="todos_jugadores")

            jugadores_label = tk.Label(recordstab, text="Jugadores", font=("Futura", 16, 'bold'))
            jugadores_label.grid(row=7, column=1, padx=20, pady=10, sticky='w')

            todos_jugadores_rb = tk.Radiobutton(recordstab, text="Todos los jugadores", variable=jugadores, value="todos_jugadores", font=("Futura", 14))
            todos_jugadores_rb.grid(row=8, column=1, padx=5, pady=2, sticky='w')
            yo_rb = tk.Radiobutton(recordstab, text="Yo", variable=jugadores, value="yo", font=("Futura", 14))
            yo_rb.grid(row=9, column=1, padx=5, pady=2, sticky='w')

            continuar = tk.Button(recordstab, text="Continuar", font=("Futura", 14), command=lambda: mostrar_records_seleccionados(records, dificultad.get(), jugadores.get()))
            continuar.grid(row=10, column=1, padx=20, pady=20)

        def iniciar_partida(nombre, estado_guardado=None):
            """Inicia una partida de Kakuro 9x9 con el nombre del jugador y un estado guardado opcional (si el jugador le dió click a cargar guardado)"""
            global guardados
    
            juegoactual_path = os.path.join(os.path.dirname(__file__), "kakuro2025_juegoactual.json")
            with open(juegoactual_path, "r") as file:
                guardados = json.load(file)

            def buscar_guardado():
                """Busca y carga la partida guardada del jugador"""
                try:
                    #va a tirar error si no hay guardados
                    juegoactual_path = os.path.join(script_dir, "kakuro2025_juegoactual.json")
                    try:
                        with open(juegoactual_path, "r") as file:
                            guardados_existentes = json.load(file)
                    except:
                        messagebox.showerror("Error", "No hay partidas guardadas")
                        return
                    
                    guardado_jugador = None
                    for guardado in guardados_existentes:
                        if guardado.get("nombre_jugador") == nombre:
                            guardado_jugador = guardado
                            break
                    
                    if not guardado_jugador:
                        messagebox.showerror("Error", f"No hay partida guardada para '{nombre}'")
                        return
                    
                    respuesta = messagebox.askyesno("Confirmar carga", "¿Está seguro de que desea cargar su partida guardada?\nVa a perder el progreso actual.")
                    if respuesta:
                        juego.destroy()
                        #crea una nueva partida con el nombre del guardado y el estado cargado
                        iniciar_partida(guardado_jugador.get("nombre_jugador", nombre), guardado_jugador)
                    
                except:
                    messagebox.showerror("Error", "Error")

            def guardar_partida():
                """Guarda el progreso actual del juego (solo uno por jugador, no stackeable)"""
                #con esto sabemos como está el juego actualmente
                estado_juego = game_logic.obtener_estado_juego()
                
                if estado_juego is None:
                    messagebox.showerror("Error", "No hay un juego activo para guardar")
                    return
                
                respuesta = messagebox.askyesno("Confirmar guardado", "¿Está seguro de que desea guardar su progreso?\n(Se sobrescribirá cualquier guardado anterior)")
                if not respuesta:
                    return
                
                #busca guardados que existan
                juegoactual_path = os.path.join(script_dir, "kakuro2025_juegoactual.json")
                try:
                    with open(juegoactual_path, "r") as file:
                        guardados_existentes = json.load(file)
                except:
                    guardados_existentes = []
                
                #quita cualquier cosa que no sea el más reciente del jugador
                guardados_existentes = [g for g in guardados_existentes if g.get("nombre_jugador") != nombre]
                
                guardados_existentes.append(estado_juego)
                with open(juegoactual_path, "w") as file:
                    json.dump(guardados_existentes, file, separators=(',', ':'))
                
                messagebox.showinfo("Éxito", "Partida guardada exitosamente")
                print("guardados", guardados_existentes)
                        
            config_path = os.path.join(script_dir, "kakuro2025_configuracion.json")

            with open(config_path, "r") as file:
                configs = json.load(file)

            global borrado, terminado
            #validaciones si el nombre no sirve
            if nombre.strip() == "":
                errores.error(antes_jugar, "Nombre sin llenar", 3, 0)
                return
            
            elif len(nombre.strip()) > 40 or len(nombre.strip()) < 2:
                errores.error(antes_jugar, "Nombre debe tener entre 1 y 40 caracteres", 3, 0)
                return
            
            cambiar_partida = True
            if estado_guardado:
                #si hay un estado guardado, cargar primero y no cambiar partida
                game_logic.resetear_total()
                game_logic.cargar_estado_juego(estado_guardado)
                cambiar_partida = False
            elif borrado:
                #resetear el juego, mantener la misma partida
                game_logic.resetear_juego()
                cambiar_partida = False
                borrado = False
            elif terminado:
                #cambiar de partida totalmente
                game_logic.resetear_total()
                cambiar_partida = True
                terminado = False
            
            antes_jugar.destroy()
            root.withdraw()
            juego = tk.Toplevel()
            juego.title("Kakuro - Jugando")
            juego.geometry("600x900") 

            titulo = tk.Label(juego, text="KAKURO", font=('Arial Black', 28, 'bold'), fg='green')
            titulo.grid(row=0, column=0, columnspan=3, pady=(10, 5))
            
            jugador_frame = tk.Frame(juego)
            jugador_frame.grid(row=1, column=0, columnspan=3, pady=(0, 10))
            jugador_label = tk.Label(jugador_frame, text=f"Jugador: {nombre}", font=('Arial', 12))
            jugador_label.grid(row=0, column=0, sticky='e')
            
            game_logic.establecer_num_seleccionado(-1)  # No hay botón seleccionado inicialmente
            
            #hace tablero
            if estado_guardado:
                tablero = game_logic.setup_juego(juego, cambiar_partida=False, usar_tablero_cargado=True)
            else:
                tablero = game_logic.setup_juego(juego, cambiar_partida=cambiar_partida)
            
            tablero.grid(row=2, column=0, columnspan=2, rowspan=9, padx=10, pady=10)
            
            #numeros
            frame, botones_nums = menus.numeros_botones(juego)
            frame.grid(row=2, column=2, rowspan=9, padx=10, pady=10, sticky='ne')
            
            #enviar botones a game_logic para que los pueda usar
            game_logic.establecer_botones(botones_nums)
            
            #si hay un estado guardado, cargarlo después de crear la UI
            if estado_guardado:
                game_logic.cargar_estado_juego(estado_guardado)
            
            #esto es para que se llame a la funcion cuando el usuario gane
            game_logic.establecer_win_callback(main, nombre)

            #borrador
            borrador_frame = tk.Frame(juego)
            borrador_frame.grid(row=11, column=2, padx=10, pady=10)
            
            #frame para todos los botones del juego
            botones_frame = tk.Frame(juego)
            botones_frame.grid(row=12, column=0, columnspan=3, pady=10)
            
            btn_iniciar = tk.Button(botones_frame, text="INICIAR\nJUEGO", font=('Arial', 10, 'bold'), 
                                   bg='gray', fg='black', width=12, height=2)
            btn_iniciar['state'] = 'disabled'
            btn_iniciar.grid(row=0, column=0, padx=5, pady=5)
            
            btn_deshacer = tk.Button(botones_frame, text="DESHACER\nJUGADA", font=('Arial', 10, 'bold'), 
                                    bg="#9AFA9A", fg='black', width=12, height=2, command=game_logic.deshacer_jugada)
            btn_deshacer.grid(row=0, column=1, padx=5, pady=5)
            
            btn_borrar = tk.Button(botones_frame, text="BORRAR\nJUEGO", font=('Arial', 10, 'bold'), 
                                  bg="#59ABFD", fg='black', width=12, height=2, command=lambda: borrar_juego(juego, nombre))
            btn_borrar.grid(row=0, column=2, padx=5, pady=5)
            
            btn_guardar = tk.Button(botones_frame, text="GUARDAR\nJUEGO", font=('Arial', 10, 'bold'), 
                                   bg="#FF8000", fg='black', width=12, height=2, command=guardar_partida)
            btn_guardar.grid(row=0, column=3, padx=5, pady=5)
            
            btn_records = tk.Button(botones_frame, text="RÉCORDS", font=('Arial', 10, 'bold'), 
                                  bg="#FFFF00", fg='black', width=12, height=2, command=lambda: mostrar_records(juego))
            btn_records.grid(row=0, column=4, padx=5, pady=5)

            btn_rehacer = tk.Button(botones_frame, text="REHACER\nJUGADA", font=('Arial', 10, 'bold'), 
                                   bg="#00C2C2", fg='black', width=12, height=2, command=game_logic.rehacer_jugada)
            btn_rehacer.grid(row=1, column=1, padx=5, pady=5)
            
            btn_terminar = tk.Button(botones_frame, text="TERMINAR\nJUEGO", font=('Arial', 10, 'bold'), 
                                    bg="#006B24", fg='black', width=12, height=2, command=lambda: terminar_juego(juego, nombre))
            btn_terminar.grid(row=1, column=2, padx=5, pady=5)
            
            btn_cargar = tk.Button(botones_frame, text="CARGAR\nJUEGO", font=('Arial', 10, 'bold'), 
                                  bg="#DB4F09", fg='black', width=12, height=2, command=buscar_guardado)
            btn_cargar.grid(row=1, column=3, padx=5, pady=5)
            
            #reloj
            tipo_reloj = configs.get("tipo_reloj")
            
            if tipo_reloj != "nousar_reloj":
                reloj_frame = tk.Frame(juego)
                reloj_frame.grid(row=13, column=0, columnspan=3, pady=10)
                
                headers = ["Horas", "Minutos", "Segundos"]
                for i, text in enumerate(headers):
                    label = tk.Label(reloj_frame, text=text, borderwidth=1, relief="solid", width=10)
                    label.grid(row=0, column=i)
                    
                horas_label = tk.Label(reloj_frame, text="00", borderwidth=1, relief="sunken", width=10)
                horas_label.grid(row=1, column=0)
                
                minutos_label = tk.Label(reloj_frame, text="00", borderwidth=1, relief="sunken", width=10)
                minutos_label.grid(row=1, column=1)
                
                segundos_label = tk.Label(reloj_frame, text="00", borderwidth=1, relief="sunken", width=10)
                segundos_label.grid(row=1, column=2)
                
                if tipo_reloj == "cronometro":
                    tiempo_total_segundos = 0
                    incrementar = True
                elif tipo_reloj == "temporizador":
                    tiempo_config = configs.get("tiempo", "00:00:00")
                    h, m, s = map(int, tiempo_config.split(":"))
                    tiempo_total_segundos = h * 3600 + m * 60 + s
                    incrementar = False
                
                #sirve para ver si el reloj corre o no
                reloj_corriendo = False
                
                def actualizar_reloj():
                    '''Con esta función actualizamos el reloj cada segundo, ya sea cronómetro o temporizador'''
                    nonlocal tiempo_total_segundos, reloj_corriendo, tipo_reloj
                    
                    if not reloj_corriendo:
                        return
                    
                    if tipo_reloj == "cronometro":
                        tiempo_total_segundos += 1
                        if tiempo_total_segundos >= 3600 * 2 + 59 * 60 + 59:
                            reloj_corriendo = False
                            messagebox.showinfo("Tiempo límite", "El cronómetro alcanzó el tiempo maximo. Se cerrará el juego en 5 segundos.") #validación por si se llaga al max
                            juego.after(5000, juego.destroy)
                            main()
                            
                    elif tipo_reloj == "temporizador":
                        if tiempo_total_segundos > 0:
                            tiempo_total_segundos -= 1
                        else:
                            #el usuario se queda sin tiempo
                            reloj_corriendo = False
                            respuesta = messagebox.askyesno("Tiempo Expirado", "¡Se acabó el tiempo! ¿Desea continuar el mismo juego?")
                            
                            if respuesta:
                                #hacemos esto para mantener el tiempo, sino cerramos
                                tiempo_config = configs.get("tiempo", "00:00:00")
                                h, m, s = map(int, tiempo_config.split(":"))
                                tiempo_temporizador_original = h * 3600 + m * 60 + s
                                
                                tipo_reloj = "cronometro"
                                tiempo_total_segundos = tiempo_temporizador_original
                                reloj_corriendo = True
                                
                                juego.after(1000, actualizar_reloj)
                            else:
                                juego.destroy()
                                main()
                            return

                    horas = tiempo_total_segundos // 3600
                    minutos = (tiempo_total_segundos % 3600) // 60
                    segundos = tiempo_total_segundos % 60
                    
                    horas_label.config(text=f"{horas:02d}")
                    minutos_label.config(text=f"{minutos:02d}")
                    segundos_label.config(text=f"{segundos:02d}")
                    
                    if reloj_corriendo:
                        juego.after(1000, actualizar_reloj)
                
                def iniciar_reloj():
                    '''Inicia el reloj, sea cronometro o temporizador'''
                    nonlocal reloj_corriendo
                    reloj_corriendo = True
                    actualizar_reloj()
                
                def pausar_reloj():
                    '''Lo pausamos, si abrimos records, o hacemos algo'''
                    nonlocal reloj_corriendo
                    reloj_corriendo = False
                
                def reiniciar_reloj():
                    '''Reiniciamos reloj, puede servir para borrar el juego'''
                    nonlocal tiempo_total_segundos, reloj_corriendo
                    reloj_corriendo = False
                    
                    if tipo_reloj == "cronometro":
                        tiempo_total_segundos = 0
                        horas_label.config(text="00")
                        minutos_label.config(text="00")
                        segundos_label.config(text="00")
                    elif tipo_reloj == "temporizador":
                        tiempo_config = configs.get("tiempo", "00:00:00")
                        h, m, s = map(int, tiempo_config.split(":"))
                        tiempo_total_segundos = h * 3600 + m * 60 + s
                        horas_label.config(text=f"{h:02d}")
                        minutos_label.config(text=f"{m:02d}")
                        segundos_label.config(text=f"{s:02d}")
                
                if tipo_reloj == "temporizador":
                    tiempo_config = configs.get("tiempo", "00:00:00")
                    h, m, s = map(int, tiempo_config.split(":"))
                    horas_label.config(text=f"{h:02d}")
                    minutos_label.config(text=f"{m:02d}")
                    segundos_label.config(text=f"{s:02d}")
                
                #esto es una forma de guardar las funciones en el juego, sumamente útil
                juego.iniciar_reloj = iniciar_reloj
                juego.pausar_reloj = pausar_reloj
                juego.reiniciar_reloj = reiniciar_reloj
            
            nivel = configs["nivel"]
            print(configs)
            match nivel:
                case "facil":
                    nivel = "FÁCIL"
                case "medio":
                    nivel = "MEDIO"
                case "dificil":
                    nivel = "DIFÍCIL"
                case "experto":
                    nivel = "EXPERTO"

            nivel_label = tk.Label(juego, text=f"NIVEL {nivel}", font=('Arial', 12, 'bold'))
            nivel_label.grid(row=14, column=0, columnspan=3, pady=5)

            #el boton de inicio
            mostrar_overlay_iniciar(juego)

    def configuracion():
        '''Con esto iniciamos la ventana de configuracón'''

        config_path = os.path.join(script_dir, "kakuro2025_configuracion.json")

        with open(config_path, "r") as file:
            configs_para_cambiar = json.load(file)

        config = tk.Toplevel()
        config.title("Kakuro - Configuración")
        config.geometry("400x640")

        config.columnconfigure(0, weight=1)
        config.columnconfigure(1, weight=1)
        config.columnconfigure(2, weight=1)
        config.columnconfigure(3, weight=1)

        titulo = tk.Label(config, text="Configuración", font=("Futura", 24))
        titulo.grid(row=0, column=1, columnspan=2, padx=20, pady=20)

        dificultad= tk.StringVar(value=f"{configs_para_cambiar['nivel']}")

        dificultad_label = tk.Label(config, text="Dificultad:", font=("Futura", 16))
        dificultad_label.grid(row=1, column=1, columnspan=2, padx=20, pady=10, sticky='w')

        facil_rb = tk.Radiobutton(config, text="Fácil", variable=dificultad, value="facil", font=("Futura", 14))
        facil_rb.grid(row=2, column=1, padx=5, pady=2, sticky='w')
        medio_rb = tk.Radiobutton(config, text="Medio", variable=dificultad, value="medio", font=("Futura", 14))
        medio_rb.grid(row=3, column=1, padx=5, pady=2, sticky='w')
        dificil_rb = tk.Radiobutton(config, text="Difícil", variable=dificultad, value="dificil", font=("Futura", 14))
        dificil_rb.grid(row=4, column=1, padx=5, pady=2, sticky='w')
        experto_rb = tk.Radiobutton(config, text="Experto", variable=dificultad, value="experto", font=("Futura", 14))
        experto_rb.grid(row=5, column=1, padx=5, pady=2, sticky='w')

        reloj_label = tk.Label(config, text="Reloj:", font=("Futura", 16))
        reloj_label.grid(row=6, column=1, columnspan=2, padx=5, pady=20, sticky='w')
        tiempo_vars = {"horas": tk.StringVar(value="0"),
                      "minutos": tk.StringVar(value="0"),
                      "segundos": tk.StringVar(value="0")}
        
        frame_temp = tk.Frame(config)
        frame_temp.grid(row=10, column=0, columnspan=4, padx=10, pady=10, sticky='w')
        frame_temp.grid_remove()

        def show_temporizador():
            frame_temp.grid()
                
            headers = ["Horas", "Minutos", "Segundos"]
            for i, text in enumerate(headers):
                label = tk.Label(frame_temp, text=text, borderwidth=1, relief="solid", width=10)
                label.grid(row=0, column=i + 1)

            spin_horas = tk.Spinbox(frame_temp, from_=0, to=2, width=10, justify='center', relief="sunken", textvariable=tiempo_vars["horas"])
            spin_horas.grid(row=1, column=1)

            spin_minutos = tk.Spinbox(frame_temp, from_=0, to=59, width=10, justify='center', relief="sunken", textvariable=tiempo_vars["minutos"])
            spin_minutos.grid(row=1, column=2)

            spin_segundos = tk.Spinbox(frame_temp, from_=0, to=59, width=10, justify='center', relief="sunken", textvariable=tiempo_vars["segundos"])
            spin_segundos.grid(row=1, column=3)
        
        def hide_temporizador():
            '''Quita el frame del temporizador'''
            frame_temp.grid_remove()
            
        def conseguir_t_str():
            '''Para pasar de tiempo a str'''
            h = tiempo_vars["horas"].get().zfill(2) # el zfill para que tenga 2 dígitos siempre
            m = tiempo_vars["minutos"].get().zfill(2)
            s = tiempo_vars["segundos"].get().zfill(2)
            return f"{h}:{m}:{s}"

        def aceptar_configuracion(dificultad, tipo_reloj):
            '''Guarda la config en el json, hace validaciones'''
            if tiempo_vars["horas"].get() == "" or tiempo_vars["minutos"].get() == "" or tiempo_vars["segundos"].get() == "":
                messagebox.showerror("Error", "Por favor, complete todos los campos de tiempo")
                return

            if (int(tiempo_vars["horas"].get()) > 2 or int(tiempo_vars["minutos"].get()) > 59 or int(tiempo_vars["segundos"].get()) > 59 or int(tiempo_vars["horas"].get()) < 0 or int(tiempo_vars["minutos"].get()) < 0 or int(tiempo_vars["horas"].get()) < 0) and tipo_reloj == "temporizador":
                messagebox.showerror("Error", "Tiempo inválido. Debe ser 0-2 horas, 0-59 minutos y 0-59 segundos")
                return

            config_path = os.path.join(os.path.dirname(__file__), "kakuro2025_configuracion.json")
            
            new_config = {
                "nivel": dificultad,
                "tipo_reloj": tipo_reloj,
                "tiempo": "00:00:00"
            }
            
            if tipo_reloj == "temporizador":
                new_config["tiempo"] = conseguir_t_str()


            with open(config_path, "w") as file:
                json.dump(new_config, file, indent=4)

            messagebox.showinfo("Éxito", "Configuración guardada exitosamente")
                
            config.destroy()
                                
                 
        tipo_reloj = tk.StringVar(value=f"{configs_para_cambiar['tipo_reloj']}")
        if tipo_reloj.get() == "temporizador":
            show_temporizador()
        
        cronometro_cb = tk.Radiobutton(config, text="Cronómetro", variable=tipo_reloj, value="cronometro", font=("Futura", 14), command=hide_temporizador)
        cronometro_cb.grid(row=7, column=1, padx=5, pady=2, sticky='w')
        
        temporizador_cb = tk.Radiobutton(config, text="Temporizador", variable=tipo_reloj, value="temporizador", font=("Futura", 14), command=show_temporizador)
        temporizador_cb.grid(row=8, column=1, padx=5, pady=2, sticky='w')
        
        sin_reloj_cb = tk.Radiobutton(config, text="No usar reloj", variable=tipo_reloj, value="nousar_reloj", font=("Futura", 14), command=hide_temporizador)
        sin_reloj_cb.grid(row=9, column=1, padx=5, pady=2, sticky='w')
        
        aceptar = tk.Button(config, text="Aceptar", font=("Futura", 14), command=lambda: aceptar_configuracion(dificultad.get(), tipo_reloj.get()))
        aceptar.grid(row=11, column=1, columnspan=2, padx=20, pady=20)


    def iniciar_ayuda():
        '''Inicia la ventana de ayuda'''
        print("Iniciando la ayuda...")

    def iniciar_acerca_de():
        '''Inicia la ventana de acerca de'''
        acercade = tk.Toplevel()
        acercade.title("Kakuro - Acerca de")
        acercade.geometry("400x130")

        info = tk.Label(acercade, text="Programa #3: Kakuro\nDesarrollado por Fabián Sánchez Durán\nTaller de Programación G5\nProfesor: William Mata Rodríguez\nI Semestre 2025", wraplength=300)
        info.pack(pady=20)

    root = tk.Tk()
    root.title("Kakuro")
    root.geometry("800x600")

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    
    #este es el menú principal
    titulo = tk.Label(root, text="Kakuro", font=("Futura", 50), fg="green")
    titulo.config()
    titulo.grid(row=0, column=1,pady=(10, 60), sticky='')

    jugar = tk.Button(root, text="Jugar", font=("Futura", 20), command=iniciar_juego)
    jugar.grid(row=1, column=1, pady=(20, 10), sticky='')

    configurar = tk.Button(root, text="Configurar", font=("Futura", 20), command=configuracion)
    configurar.grid(row=2, column=1, pady=(5, 10), sticky='')

    ayuda = tk.Button(root, text="Ayuda", font=("Futura", 20), command=iniciar_ayuda)
    ayuda.grid(row=3, column=1, pady=(5, 10), sticky='')

    acercade = tk.Button(root, text="Acerca de", font=("Futura", 20), command=iniciar_acerca_de)
    acercade.grid(row=4, column=1, pady=(5, 10), sticky='')

    salir = tk.Button(root, text="Salir", font=("Futura", 20), command=root.destroy)
    salir.grid(row=5, column=1, pady=(5, 10), sticky='')

    root.mainloop()

main()


def terminar_juego_ganar(window=None):     
    '''Nos sirve cuando el jugador gana, la pongo afuera porque la vamos a ocupar en game_logic.py'''
    if window:
        window.destroy()
    main()
