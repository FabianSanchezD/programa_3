import os
import sys

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modulos'))
sys.path.append(file_path)
import errores

'''
Instituto Tecnológico de Costa Rica

Programa #3: Kakuro

Fabián Sánchez Durán

Profesor: William Mata Rodríguez

I Semestre 2025
'''

import tkinter as tk

#Función prinicipal del programa
def main():

    #Va a iniciar el juego
    def iniciar_juego():
        antes_jugar = tk.Toplevel()
        antes_jugar.title("Kakuro - Antes de Jugar")
        antes_jugar.geometry("360x200")

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
            juego.geometry("800x800")

            columns = 6
            for i in range(columns):
                juego.columnconfigure(i, weight=1)

            inicio = tk.Label(juego, text="Kakuro", font=('Futura', 40), fg='green')
            inicio.grid(row=0, column=0, padx=(5, 20), pady=10, columnspan=2)

            nombre = tk.Label(juego, text=f"Jugador: {nombre}", font=('Futura', 17))
            nombre.grid(row=0, column=2, padx=20, pady=10, columnspan=3, sticky='w')



    #Va a iniciar la configuración
    def configuracion():
        print("Configurando el juego...")

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