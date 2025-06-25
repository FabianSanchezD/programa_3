'''
Instituto Tecnológico de Costa Rica

Programa #3: Kakuro

Fabián Sánchez Durán

Profesor: William Mata Rodríguez

I Semestre 2025
'''
import os
import json
import sys
from tkinter import messagebox

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modulos import errores
from src import game_logic
from src import menus
import tkinter as tk

#Función prinicipal del programa
def main():

    script_dir = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(script_dir, "kakuro2025_configuracion.json")

    with open(config_path, "r") as file:
        configs = json.load(file)

    #Va a iniciar el juego
    def iniciar_juego():
        antes_jugar = tk.Toplevel()
        antes_jugar.title("Kakuro - Antes de Jugar")
        antes_jugar.geometry("360x250")

        info = tk.Label(antes_jugar, text="Antes de jugar, ¿cuál es su nombre?", font=("Futura", 14))
        info.grid(row=0, column=0, padx=20, pady=20)

        nombre_entry = tk.Entry(antes_jugar, font=("Futura", 12))
        nombre_entry.grid(row=1, column=0, padx=20, pady=10)

        continuar = tk.Button(antes_jugar, text="Continuar", font=("Futura", 12), command=lambda: iniciar_partida(nombre_entry.get()))
        continuar.grid(row=2, column=0, padx=20, pady=10)
        
        def iniciar_partida(nombre):
            if nombre.strip() == "":
                errores.error(antes_jugar, "Nombre sin llenar", 3, 0)
                return
            
            elif len(nombre.strip()) > 40 or len(nombre.strip()) < 2:
                errores.error(antes_jugar, "Nombre debe tener entre 1 y 40 caracteres", 3, 0)
                return
            
            antes_jugar.destroy()
            root.withdraw()
            juego = tk.Toplevel()
            juego.title("Kakuro - Jugando")
            juego.geometry("600x850") 

            # Título Kakuro
            titulo = tk.Label(juego, text="KAKURO", font=('Arial Black', 28, 'bold'), fg='green')
            titulo.grid(row=0, column=0, columnspan=3, pady=(10, 5))
            
            # Campo para nombre del jugador
            jugador_frame = tk.Frame(juego)
            jugador_frame.grid(row=1, column=0, columnspan=3, pady=(0, 10))
            jugador_label = tk.Label(jugador_frame, text=f"Jugador: {nombre}", font=('Arial', 12))
            jugador_label.grid(row=0, column=0, sticky='e')
            
            game_logic.establecer_num_seleccionado(0)
            
            # Tablero
            tablero = game_logic.setup_juego(juego)
            tablero.grid(row=2, column=0, columnspan=2, rowspan=9, padx=10, pady=10)
            
            # Botones de números
            frame, botones_nums = menus.numeros_botones(juego)
            frame.grid(row=2, column=2, rowspan=9, padx=10, pady=10, sticky='ne')

            # Botón borrador
            borrador_frame = tk.Frame(juego)
            borrador_frame.grid(row=11, column=2, padx=10, pady=10)
            
            # Botones de acción
            botones_frame = tk.Frame(juego)
            botones_frame.grid(row=12, column=0, columnspan=3, pady=10)
            
            # Primera fila de botones
            btn_iniciar = tk.Button(botones_frame, text="INICIAR\nJUEGO", font=('Arial', 10, 'bold'), 
                                   bg='gray', fg='black', width=12, height=2)
            btn_iniciar['state'] = 'disabled'
            btn_iniciar.grid(row=0, column=0, padx=5, pady=5)
            
            btn_deshacer = tk.Button(botones_frame, text="DESHACER\nJUGADA", font=('Arial', 10, 'bold'), 
                                    bg="#9AFA9A", fg='black', width=12, height=2)
            btn_deshacer.grid(row=0, column=1, padx=5, pady=5)
            
            btn_borrar = tk.Button(botones_frame, text="BORRAR\nJUEGO", font=('Arial', 10, 'bold'), 
                                  bg="#59ABFD", fg='black', width=12, height=2)
            btn_borrar.grid(row=0, column=2, padx=5, pady=5)
            
            btn_guardar = tk.Button(botones_frame, text="GUARDAR\nJUEGO", font=('Arial', 10, 'bold'), 
                                   bg="#FF8000", fg='black', width=12, height=2)
            btn_guardar.grid(row=0, column=3, padx=5, pady=5)
            
            btn_records = tk.Button(botones_frame, text="RÉCORDS", font=('Arial', 10, 'bold'), 
                                  bg="#FFFF00", fg='black', width=12, height=2)
            btn_records.grid(row=0, column=4, padx=5, pady=5)
            
            # Segunda fila de botones
            btn_rehacer = tk.Button(botones_frame, text="REHACER\nJUGADA", font=('Arial', 10, 'bold'), 
                                   bg="#00C2C2", fg='black', width=12, height=2)
            btn_rehacer.grid(row=1, column=1, padx=5, pady=5)
            
            btn_terminar = tk.Button(botones_frame, text="TERMINAR\nJUEGO", font=('Arial', 10, 'bold'), 
                                    bg="#006B24", fg='black', width=12, height=2)
            btn_terminar.grid(row=1, column=2, padx=5, pady=5)
            
            btn_cargar = tk.Button(botones_frame, text="CARGAR\nJUEGO", font=('Arial', 10, 'bold'), 
                                  bg="#DB4F09", fg='black', width=12, height=2)
            btn_cargar.grid(row=1, column=3, padx=5, pady=5)
            
            # Reloj
            reloj_frame = tk.Frame(juego)
            reloj_frame.grid(row=13, column=0, columnspan=3, pady=10)
            
            headers = ["Horas", "Minutos", "Segundos"]
            for i, text in enumerate(headers):
                label = tk.Label(reloj_frame, text=text, borderwidth=1, relief="solid", width=10)
                label.grid(row=0, column=i)
                
            horas = tk.Label(reloj_frame, text="00", borderwidth=1, relief="sunken", width=10)
            horas.grid(row=1, column=0)
            
            minutos = tk.Label(reloj_frame, text="00", borderwidth=1, relief="sunken", width=10)
            minutos.grid(row=1, column=1)
            
            segundos = tk.Label(reloj_frame, text="00", borderwidth=1, relief="sunken", width=10)
            segundos.grid(row=1, column=2)
            
            # Nivel
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

            overlay = tk.Toplevel(juego)
            overlay.title("Kakuro - Jugando")
            tk.Button(overlay, text="INICIAR JUEGO", font=("Futura",20), bg='green', command=overlay.destroy).pack(pady=450)
            overlay.grab_set() 
            overlay.transient(juego) 
            
            juego.update_idletasks()

            juego_x = juego.winfo_x()
            juego_y = juego.winfo_y()
            juego_width = juego.winfo_width()
            juego_height = juego.winfo_height()

            overlay_width = 600
            overlay_height = 850
            overlay.geometry(f"{overlay_width}x{overlay_height}+{juego_x + (juego_width - overlay_width)//2}+{juego_y + (juego_height - overlay_height)//2}")

    #Va a iniciar la configuración
    def configuracion():
        config = tk.Toplevel()
        config.title("Kakuro - Configuración")
        config.geometry("400x640")

        config.columnconfigure(0, weight=1)
        config.columnconfigure(1, weight=1)
        config.columnconfigure(2, weight=1)
        config.columnconfigure(3, weight=1)

        titulo = tk.Label(config, text="Configuración", font=("Futura", 24))
        titulo.grid(row=0, column=1, columnspan=2, padx=20, pady=20)

        dificultad= tk.StringVar(value="facil")

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

            spin_horas = tk.Spinbox(frame_temp, from_=0, to=2, width=10, justify='center', textvariable=tiempo_vars["horas"])
            spin_horas.grid(row=1, column=1)

            spin_minutos = tk.Spinbox(frame_temp, from_=0, to=59, width=10, justify='center', textvariable=tiempo_vars["minutos"])
            spin_minutos.grid(row=1, column=2)

            spin_segundos = tk.Spinbox(frame_temp, from_=0, to=59, width=10, justify='center', textvariable=tiempo_vars["segundos"])
            spin_segundos.grid(row=1, column=3)
        
        def hide_temporizador():
            frame_temp.grid_remove()
            
        def conseguir_t_str():
            h = tiempo_vars["horas"].get().zfill(2) # el zfill para que tenga 2 dígitos siempre
            m = tiempo_vars["minutos"].get().zfill(2)
            s = tiempo_vars["segundos"].get().zfill(2)
            return f"{h}:{m}:{s}"

        def aceptar_configuracion(dificultad, tipo_reloj):
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
                                
                 
        tipo_reloj = tk.StringVar(value="cronometro")
        
        cronometro_cb = tk.Radiobutton(config, text="Cronómetro", variable=tipo_reloj, value="cronometro", font=("Futura", 14), command=hide_temporizador)
        cronometro_cb.grid(row=7, column=1, padx=5, pady=2, sticky='w')
        
        temporizador_cb = tk.Radiobutton(config, text="Temporizador", variable=tipo_reloj, value="temporizador", font=("Futura", 14), command=show_temporizador)
        temporizador_cb.grid(row=8, column=1, padx=5, pady=2, sticky='w')
        
        sin_reloj_cb = tk.Radiobutton(config, text="No usar reloj", variable=tipo_reloj, value="nousar_reloj", font=("Futura", 14), command=hide_temporizador)
        sin_reloj_cb.grid(row=9, column=1, padx=5, pady=2, sticky='w')
        
        aceptar = tk.Button(config, text="Aceptar", font=("Futura", 14), command=lambda: aceptar_configuracion(dificultad.get(), tipo_reloj.get()))
        aceptar.grid(row=11, column=1, columnspan=2, padx=20, pady=20)



    #Va a iniciar la ayuda
    def iniciar_ayuda():
        print("Iniciando la ayuda...")

    #Va a iniciar la sección de acerca de
    def iniciar_acerca_de():
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
