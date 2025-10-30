import tkinter as tk
from tkinter import ttk

# 1. Crear la ventana
ventana = tk.Tk()
ventana.title("Tabla de empleados")
ventana.geometry("400x250")

# 2. Definir las columnas
columnas = ("id", "nombre", "cargo")
tabla = ttk.Treeview(ventana, columns=columnas, show="headings")

# 3. Configurar los encabezados
tabla.heading("id", text="ID")
tabla.heading("nombre", text="Nombre")
tabla.heading("cargo", text="Cargo")

# 4. Configurar el ancho de las columnas
tabla.column("id", width=50, anchor="center")
tabla.column("nombre", width=150, anchor="w")
tabla.column("cargo", width=150, anchor="w")

# 5. Insertar datos
datos = [
    (1, "Ana Pérez", "Gerente"),
    (2, "Luis Gómez", "Desarrollador"),
    (3, "Marta Ruiz", "Diseñadora"),
    (4, "Carlos Sánchez", "Contador")
]

for fila in datos:
    tabla.insert("", tk.END, values=fila)

# 6. Añadir la tabla a la ventana
tabla.pack(padx=10, pady=10, expand=True, fill="both")

# 7. Ejecutar el bucle principal
ventana.mainloop()

