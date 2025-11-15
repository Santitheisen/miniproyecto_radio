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
imagen = Image.open("imagenes/Spinettabajan.jpg")
imagen = imagen.resize((100,100))
imagentk = ImageTk.PhotoImage(imagen)
etiqueta_imagen = tk.Label(ventana,image=imagentk,bd=5,relief=tk.SUNKEN, anchor="center")
etiqueta_imagen.place(relx=0.5, rely=0.33, anchor='center')

#Un diccionario donde las claves son los interpretes y el valor es una lista de canciones de su respectivo inteprete o clave

ruta_base = os.path.dirname(os.path.abspath(__file__))
imagenes = os.path.join(ruta_base, "imagenes")

canciones = {
    "Alejandro Fernández": {
        "Me Dediqué a Perderte": os.path.join(imagenes, "alejandro_perderte.jpg"),
        "Se Me Va la Voz": os.path.join(imagenes, "alejandro_voz.jpg"),
        "Nube Viajera": os.path.join(imagenes, "alejandro_nube.jpg")
    },
    "Luis Miguel":{
        "Suave": os.path.join(imagenes, "Luismiguelsuave.jpg"),
        "Sabor a mi": os.path.join(imagenes, "Luismiguelsaborami.jpg"),
        "La incondicional": os.path.join(imagenes,"Luismiguellaincondicional.jpg") ,
        "No culpes a la noche": os.path.join(imagenes, "Luismiguelnoculpesalanoche.jpg"),
    }
    }


entrada_interprete = ttk.Combobox(ventana, values=list(canciones.keys()), width=37, state='readonly')
entrada_interprete.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
entrada_interprete.set("Elegir Intérprete")  

etiqueta_cancion = tk.Label(ventana, text="Canción", font=("Arial", 10))
etiqueta_cancion.grid(row=2, column=0, padx=10, pady=10)

entrada_cancion = ttk.Combobox(ventana, values= [], width=37, state='readonly')
entrada_cancion.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
entrada_cancion.set("Elegir canción")

def mostrar_canciones(event):
    artista_seleccionado = entrada_interprete.get()
    if artista_seleccionado in canciones:
        entrada_cancion["values"] = canciones[artista_seleccionado]
        entrada_cancion.set("Elegir canción")


def mostrar_imagen(event):
    imagen_album = entrada_cancion.get()
    

entrada_interprete.bind("<<ComboboxSelected>>", mostrar_canciones, mostrar_imagen)















ventana.mainloop()