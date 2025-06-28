import tkinter as tk #para hacer gui
import sys #para importar módulos
import os #para importar módulos x2

#añadimos la ruta del proyecto para poder importar módulos correctamente
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import game_logic #para tener logica del juego
botones = []

def numeros_botones(root, tamano=9, num_seleccionado=None):
    '''Crea botones numerados del 1 al tamaño (en todos los casos 9, pero mejor no hacer hardcode)'''
    global botones
    botones = []  #resetear la lista de botones cada vez que se crea
    frame = tk.Frame(root)
    frame.grid(row=1, column=7, rowspan=9, padx=10, pady=10, sticky="n")
    
    for i in range(1, tamano + 1):
        if i == num_seleccionado:
            bg_color = "#00CED1"
        else:
            bg_color = "white"
        
        button_frame = tk.Frame(frame, bd=0, highlightthickness=0)
        button_frame.pack(pady=5)
        
        canvas = tk.Canvas(button_frame, width=60, height=40, bd=0, highlightthickness=0)
        canvas.pack()
        
        canvas.create_rectangle(10, 0, 50, 40, fill=bg_color, outline="black")
        
        canvas.create_text(30, 20, text=f"{i}", font=("Futura", 16))
        
        botones.append((canvas, i))
        
        canvas.bind("<Button-1>", lambda e, num=i: onClick(num)) #le bindeamos el click a la funcion onClick

    print(botones)
    
    def onClick(number):
        '''Función que se ejecuta al hacer click en un botón, hace que se escriba el número'''
        for btn, num in botones:
            btn.delete("all")
            btn.create_rectangle(10, 0, 50, 40, fill="white", outline="black")
            btn.create_text(30, 20, text=f"{num}", font=("Futura", 16))
            
        clicked_btn = botones[number-1][0]
        clicked_btn.delete("all")
        clicked_btn.create_rectangle(10, 0, 50, 40, fill="#00CED1", outline="black")
        clicked_btn.create_text(30, 20, text=f"{number}", font=("Futura", 16))
        
        print(f"Seleccionó {number}")
        
        game_logic.establecer_num_seleccionado(number)
        
        return number
    
    borrador = tk.Frame(frame, bd=0, highlightthickness=0)
    borrador.pack(pady=15)
    
    eraser_canvas = tk.Canvas(borrador, width=60, height=30, bd=0, highlightthickness=0)
    eraser_canvas.pack()
    
    eraser_canvas.create_rectangle(5, 10, 40, 25, fill="#FF6347", outline="black") 
    eraser_canvas.create_rectangle(40, 10, 55, 25, fill="#4682B4", outline="black") 
    
    eraser_canvas.bind("<Button-1>", lambda e: click_borrador()) #bindeamos el click al borrador
    
    def click_borrador():
        '''Función que se ejecuta al hacer click en el borrador, hace que se borre el número seleccionado'''
        for btn, num in botones:
            btn.delete("all")
            btn.create_rectangle(10, 0, 50, 40, fill="white", outline="black")
            btn.create_text(30, 20, text=str(num), font=("Arial", 16))
        
        print("Seleccionó el borrador")

        game_logic.establecer_num_seleccionado(0)
        return 0 
    
    
    return frame, botones


