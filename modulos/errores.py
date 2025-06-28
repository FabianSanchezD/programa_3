import tkinter as tk

#modulo muy simple para mostrar errores con solo una linea de código, se utilizó solo en una parte (pedir nombre, luego usé messagebox de tkinter)
def error(ventana, mensaje, row, column):
    error = tk.Label(ventana, text=f"ERROR: {mensaje}.", fg="red", font=("Futura", 12), wraplength=300)
    error.grid(row=row, column=column, padx=20, pady=10)