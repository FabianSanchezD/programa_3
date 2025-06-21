import tkinter as tk

def numeros_botones(root, tamano=9, num_seleccionado=None):
    frame = tk.Frame(root)
    frame.grid(row=1, column=7, rowspan=9, padx=10, pady=10, sticky="n")
    
    botones = []
    
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
        
        canvas.bind("<Button-1>", lambda e, num=i: onClick(num)) #REVISAR ESO
        
    def onClick(number):
        for btn, num in botones:
            btn.delete("all")
            btn.create_rectangle(10, 0, 50, 40, fill="white", outline="black")
            btn.create_text(30, 20, text=f"{num}", font=("Futura", 16))
            
        clicked_btn = botones[number-1][0]
        clicked_btn.delete("all")
        clicked_btn.create_rectangle(10, 0, 50, 40, fill="#00CED1", outline="black")
        clicked_btn.create_text(30, 20, text=f"{number}", font=("Futura", 16))
        
        print(f"Seleccionó {number}")

        return number
    
    borrador = tk.Frame(frame, bd=0, highlightthickness=0)
    borrador.pack(pady=15)
    
    eraser_canvas = tk.Canvas(borrador, width=60, height=30, bd=0, highlightthickness=0)
    eraser_canvas.pack()
    
    eraser_canvas.create_rectangle(5, 10, 40, 25, fill="#FF6347", outline="black") 
    eraser_canvas.create_rectangle(40, 10, 55, 25, fill="#4682B4", outline="black") 
    
    eraser_canvas.bind("<Button-1>", lambda e: click_borrador()) #REVISAR ESO
    
    def click_borrador():
        for btn, num in botones:
            btn.delete("all")
            btn.create_rectangle(10, 0, 50, 40, fill="white", outline="black")
            btn.create_text(30, 20, text=str(num), font=("Arial", 16))
        
        print("Seleccionó el borrador")
        return 0 
    
    return frame, botones

