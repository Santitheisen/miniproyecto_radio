import tkinter as tk
from tkinter import ttk

def manejar_cambio(event):
    # La variable 'seleccion' ahora tiene el nuevo valor
    print(f"Opción seleccionada: {seleccion.get()}")

# 1. Crear ventana principal
root = tk.Tk()
root.title("Ejemplo de Combobox")

# 2. Declarar la variable de control
seleccion = tk.StringVar()

# 3a. Crear la lista de opciones
opciones_disponibles = ["Rojo", "Verde", "Azul", "Amarillo"]

# 3b. Instanciar el Combobox
combo_colores = ttk.Combobox(
    root,
    textvariable=seleccion,
    values=opciones_disponibles,
    state="readonly" 
)

# 4a. Establecer un valor inicial
seleccion.set("Selecciona un color") 

# 4b. Asociar la función de manejo de eventos
combo_colores.bind("<<ComboboxSelected>>", manejar_cambio)

# 3c. Posicionar el widget
combo_colores.pack(pady=20, padx=20)

root.mainloop()

