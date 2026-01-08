import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

ventana= tk.Tk()
ventana.title("Pedidos de canciones") #titulo de la ventana
ventana.geometry("600x600") # proporciones de la ventana
ventana.grid_columnconfigure(1, weight=1)

etiqueta_oyente = tk.Label(ventana, text="Oyente", font=("Arial", 10))
etiqueta_oyente.grid(row=0, column=0, padx=10, pady=10)

entrada_oyente = tk.Entry(ventana, width=60) 
entrada_oyente.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

etiqueta_interprete = tk.Label(ventana, text="Intérprete", font=("Arial", 10))
etiqueta_interprete.grid(row=1, column=0, padx=10, pady=10)

#vamos a mostrar la imagen del album de la cancion elegida y le damos un borde
ruta_global= os.path.dirname(os.path.abspath(__file__))
imagen = os.path.join(ruta_global,"imagenes")

fondo_gris = ImageTk.PhotoImage(Image.new('RGB', (150, 150), color = 'gray')) 
etiqueta_imagen = ttk.Label(ventana, image=fondo_gris)
etiqueta_imagen.image = fondo_gris # Importante para evitar que la imagen sea eliminada por el recolector de basura
etiqueta_imagen.place(relx=0.5, rely=0.3355555, anchor="center")

#Un diccionario donde las claves son los interpretes y el valor es una lista de canciones de su respectivo inteprete o clave
catalogo = {
    "Alejandro Fernández": {
        "Me Dediqué a Perderte": os.path.join(imagen, "alejandro_perderte.jpg"),
        "Se Me Va la Voz": os.path.join(imagen, "alejandro_voz.jpg"),
        "Nube Viajera": os.path.join(imagen, "alejandro_nube.jpg")
    },
    "Shakira": {
        "Waka Waka (This Time for Africa)": os.path.join(imagen, "shakira_waka.jpg"),
        "Ciega, Sordomuda": os.path.join(imagen, "shakira_ciega.jpg"),
        "Te Felicito": os.path.join(imagen, "shakira_tefelicito.jpg")
    },
    "Luis Miguel": {
        "La Incondicional": os.path.join(imagen, "luismi_incondicional.jpg"),
        "Hasta Que Me Olvides": os.path.join(imagen, "luismi_olvides.jpg"),
        "Culpable o No": os.path.join(imagen, "luismi_culpable.jpg")
    },
    "Spinetta" : {
        "Bajan" : os.path.join(imagen, "Spinettabajan.jpg"),
        "Postcruxificción":os.path.join(imagen, "Spinettapostcruxificcion.jpg"),
        "Seguir viviendo sin tu amor" : os.path.join(imagen, "Spinettaseguirviviendosintuamor.jpg")
    }
}

entrada_interprete = ttk.Combobox(ventana, values=list(catalogo.keys()), width=37, state='readonly')
entrada_interprete.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
entrada_interprete.set("Elegir Intérprete")  

etiqueta_cancion = tk.Label(ventana, text="Canción", font=("Arial", 10))
etiqueta_cancion.grid(row=2, column=0, padx=10, pady=10)

entrada_cancion = ttk.Combobox(ventana, values= [], width=37, state='readonly')
entrada_cancion.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
entrada_cancion.set("Elegir canción")

def mostrar_canciones(event):
    artista_seleccionado = entrada_interprete.get()
    if artista_seleccionado in catalogo:
        entrada_cancion["values"] = sorted (catalogo[artista_seleccionado].keys())
        entrada_cancion.set("Elegir canción")
        etiqueta_imagen.config(image="") #borramos la imagen seleccionada si cambiamos de artista
        etiqueta_imagen.image = None #vuelve al fondo gris

def mostrar_imagen(event):
    artista = entrada_interprete.get()
    cancion = entrada_cancion.get()
    if artista in catalogo and cancion in catalogo[artista]:
        ruta_imagen = catalogo[artista][cancion]
        if os.path.exists(ruta_imagen):
            imagen_pil = Image.open(ruta_imagen) #abrimos la imagen
            imagen_pil = imagen_pil.resize((150, 150), Image.Resampling.LANCZOS) #redimensionamos
            imagen_tk = ImageTk.PhotoImage(imagen_pil) #compatibilizamos con tkinter
            etiqueta_imagen.place(relx=0.5, rely=0.3355555, anchor="center")
            etiqueta_imagen.config(image=imagen_tk)
            etiqueta_imagen.image = imagen_tk 

            

entrada_interprete.bind("<<ComboboxSelected>>", mostrar_canciones)
entrada_cancion.bind("<<ComboboxSelected>>", mostrar_imagen)












ventana.mainloop()