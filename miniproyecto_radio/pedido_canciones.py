# Importamos los módulos necesarios
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk 
import os 

# --- 1. DATOS GLOBALES Y ESTRUCTURAS DE ESTADO ---

CATALOGO = {
    "Alejandro Fernández": {
        "Me Dediqué a Perderte": "imagenes/alejandro_perderte.jpg",
        "Se Me Va la Voz": "imagenes/alejandro_voz.jpg",
        "Nube Viajera": "imagenes/alejandro_nube.jpg"
    },
    "Shakira": {
        "Waka Waka (This Time for Africa)": "imagenes/shakira_waka.jpg",
        "Ciega, Sordomuda": "imagenes/shakira_ciega.jpg",
        "Te Felicito": "imagenes/shakira_tefelicito.jpg"
    },
    "Luis Miguel": {
        "La Incondicional": "imagenes/luismi_incondicional.jpg",
        "Hasta Que Me Olvides": "imagenes/luismi_olvides.jpg",
        "Culpable o No": "imagenes/luismi_culpable.jpg"
    }
}
INTERPRETES = sorted(CATALOGO.keys())

# Variables de estado globales
LISTA_PEDIDOS_COLA = [] 
IMAGE_CACHE = {} 
IMAGEN_ALBUM_TK = None # Variable global para la referencia de imagen (Tkinter necesita esto)

# Configuración de interfaz
TAMANO_MINIATURA = (20, 20) 
TAMANO_PREVISUALIZACION = (100, 100) 
RUTA_IMAGEN_POR_DEFECTO = "imagenes/default_album.png" 

# Referencias a widgets y variables de Tkinter (TODAS SON GLOBALES)
ROOT = None
OYENTE_NOMBRE = None
INTERPRETE_SELECCIONADO = None
CANCION_SELECCIONADA = None
LABEL_CARATULA = None
TREE_COLA = None
ENTRY_OYENTE = None
COMBO_INTERPRETE = None
COMBO_CANCION = None

# --- 2. FUNCIONES DE UTILIDAD (SETUP E IMÁGENES) ---

def cargar_y_mostrar_imagen(ruta_archivo, label_widget, size):
    """Carga, redimensiona y muestra una imagen"""
    # Usamos la variable global IMAGEN_ALBUM_TK para evitar que la imagen sea recolectada por el GC
    global IMAGEN_ALBUM_TK 
    
    ruta_real = ruta_archivo 
    
    try:
        img_pil = Image.open(ruta_real)
        img_pil = img_pil.resize(size, Image.Resampling.LANCZOS)
        IMAGEN_ALBUM_TK = ImageTk.PhotoImage(img_pil)
        label_widget.config(image=IMAGEN_ALBUM_TK, text="")
    except Exception:
        # Recurre a la imagen por defecto
        try:
            img_pil = Image.open(RUTA_IMAGEN_POR_DEFECTO)
            img_pil = img_pil.resize(size, Image.Resampling.LANCZOS)
            IMAGEN_ALBUM_TK = ImageTk.PhotoImage(img_pil)
            label_widget.config(image=IMAGEN_ALBUM_TK, text="")
        except Exception:
            label_widget.config(image="", text="Carátula no disp.")
            IMAGEN_ALBUM_TK = None

def cargar_imagen_para_treeview(ruta_archivo):
    """Carga una imagen para el Treeview, recurriendo al default """
    if ruta_archivo in IMAGE_CACHE:
        return IMAGE_CACHE[ruta_archivo]

    ruta_real = ruta_archivo
    
    try:
        img_pil = Image.open(ruta_real)
        img_pil = img_pil.resize(TAMANO_MINIATURA, Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_pil)
        IMAGE_CACHE[ruta_archivo] = img_tk 
        return img_tk
    except Exception:
        # Si la imagen falla, se intenta cargar la por defecto
        try:
            return cargar_imagen_para_treeview(RUTA_IMAGEN_POR_DEFECTO)
        except Exception:
             return None 

def actualizar_imagen_album(event=None):
    """Actualiza la previsualización grande al seleccionar una canción."""
    interprete = INTERPRETE_SELECCIONADO.get()
    cancion = CANCION_SELECCIONADA.get()
    
    ruta_imagen = RUTA_IMAGEN_POR_DEFECTO
    
    if interprete in CATALOGO and cancion in CATALOGO[interprete]:
        ruta_imagen = CATALOGO[interprete][cancion]
        
    cargar_y_mostrar_imagen(ruta_imagen, LABEL_CARATULA, TAMANO_PREVISUALIZACION)

def actualizar_canciones(event):
    """Actualiza el Combobox de Canciones."""
    interprete = INTERPRETE_SELECCIONADO.get()
    
    if interprete and interprete in CATALOGO:
        canciones = sorted(CATALOGO[interprete].keys())
        
        COMBO_CANCION['values'] = canciones
        
        if canciones:
            CANCION_SELECCIONADA.set(canciones[0])
            COMBO_CANCION['state'] = 'readonly'
        else:
            CANCION_SELECCIONADA.set("")
            COMBO_CANCION['state'] = 'disabled'
    else:
        CANCION_SELECCIONADA.set("")
        COMBO_CANCION['values'] = []
        COMBO_CANCION['state'] = 'disabled'
        
    actualizar_imagen_album() 

# --- 3. FUNCIONES DE LÓGICA DE PEDIDOS ---

def realizar_pedido():
    """Añade la canción a la cola de emisión (Treeview)."""
    global LISTA_PEDIDOS_COLA 
    oyente = OYENTE_NOMBRE.get().strip() 
    interprete = INTERPRETE_SELECCIONADO.get()
    cancion = CANCION_SELECCIONADA.get()

    if not oyente or not interprete or not cancion:
        messagebox.showwarning("Falta Información", "Completa Oyente, Intérprete y Canción.")
        return

    # 1. Obtener la ruta de la imagen
    try:
        ruta_imagen = CATALOGO[interprete][cancion]
    except KeyError:
        messagebox.showerror("Error", "Canción no encontrada en el catálogo.")
        return

    # 2. Inserción en la Cola de Emisión (Treeview)
    miniatura_tk = cargar_imagen_para_treeview(ruta_imagen)
    
    texto_con_separacion = "    " + cancion
    
    # Capturo el identificador que el Widget TREE_COLA genera para la nueva fila.
    # Por si se necesito consultar mas tarde
    # Con TREE_COLA.insert inserto una nueva fila en el TREEVIEW

    item_id = TREE_COLA.insert("", "end", 
                              text=texto_con_separacion, 
                              values=(interprete, oyente), 
                              image=miniatura_tk) 
    
    # 3. Guardar los datos del pedido en la lista interna
    pedido_data = {"id": item_id, "cancion": cancion, "artista": interprete, "oyente": oyente}
    LISTA_PEDIDOS_COLA.append(pedido_data) 
    
    # Limpiar campo de oyente y enfocar
    OYENTE_NOMBRE.set("")
    ENTRY_OYENTE.focus()
    
    messagebox.showinfo("Pedido Confirmado", f"Solicitud de {oyente} agregada: {cancion}")

def cancelar_ultimo_pedido():
    """Busca y cancela el último pedido realizado en la cola (función de deshacer)."""
    global LISTA_PEDIDOS_COLA
    
    if not LISTA_PEDIDOS_COLA:
        messagebox.showinfo("Atención", "No hay pedidos pendientes en la cola para cancelar.")
        return

    # 1. Obtener el último pedido de la cola sin removerlo aún
    pedido_a_borrar = LISTA_PEDIDOS_COLA[-1]
    nombre_cancion = pedido_a_borrar['cancion']
    nombre_oyente = pedido_a_borrar['oyente']
    item_id = pedido_a_borrar['id']
    
    # 2. Pedir confirmación
    confirmacion = messagebox.askyesno(
        "Confirmar Cancelación",
        f"¿Estás seguro de que deseas CANCELAR el ÚLTIMO pedido realizado:\n\n"
        f"🎵 {nombre_cancion} ({pedido_a_borrar['artista']})\n"
        f"👤 por {nombre_oyente}?"
    )
    
    if confirmacion:
        # 3. Eliminar de la lista interna (pop del final)
        LISTA_PEDIDOS_COLA.pop()
        
        # 4. Eliminar del Treeview
        TREE_COLA.delete(item_id)
            
        messagebox.showinfo("Cancelado", f"El último pedido ({nombre_cancion} por {nombre_oyente}) ha sido cancelado.")

# --- 4. FUNCIÓN PRINCIPAL DE INTERFAZ ---

def crear_interfaz_principal(master):
    """Define y coloca todos los widgets en la ventana principal."""
    global OYENTE_NOMBRE, INTERPRETE_SELECCIONADO, CANCION_SELECCIONADA
    global LABEL_CARATULA, TREE_COLA, ENTRY_OYENTE, COMBO_INTERPRETE, COMBO_CANCION

    master.title("Pedido de Canciones 📻")
    master.columnconfigure(1, weight=1)

    # Variables de Tkinter
    OYENTE_NOMBRE = tk.StringVar()
    INTERPRETE_SELECCIONADO = tk.StringVar()
    CANCION_SELECCIONADA = tk.StringVar()

    # --- Sección de ENTRADA/SELECCIÓN ---
    
    frame_oyente = ttk.Frame(master)
    frame_oyente.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    
    ttk.Label(frame_oyente, text="Oyente:").pack(side=tk.LEFT, padx=(0, 5))
    ENTRY_OYENTE = ttk.Entry(frame_oyente, textvariable=OYENTE_NOMBRE)
    ENTRY_OYENTE.pack(side=tk.LEFT, expand=True, fill=tk.X)
    
    ttk.Label(master, text="Intérprete:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    COMBO_INTERPRETE = ttk.Combobox(master, 
                                     textvariable=INTERPRETE_SELECCIONADO, 
                                     values=INTERPRETES, 
                                     state="readonly")
    COMBO_INTERPRETE.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    COMBO_INTERPRETE.bind("<<ComboboxSelected>>", actualizar_canciones)

    ttk.Label(master, text="Canción:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    COMBO_CANCION = ttk.Combobox(master, 
                                  textvariable=CANCION_SELECCIONADA, 
                                  values=[], 
                                  state="disabled")
    COMBO_CANCION.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    COMBO_CANCION.bind("<<ComboboxSelected>>", actualizar_imagen_album)
    
    # Carátula y Botón de Pedido
    frame_visualizacion = ttk.Frame(master)
    frame_visualizacion.grid(row=3, column=0, columnspan=2, pady=10)
    
    LABEL_CARATULA = ttk.Label(frame_visualizacion, text="Carátula Aquí")
    LABEL_CARATULA.pack(side=tk.LEFT, padx=15)
    
    ttk.Button(frame_visualizacion, text="Solicitar Canción 🎶", command=realizar_pedido).pack(side=tk.LEFT, padx=15)

    # --- Sección de COLA DE EMISIÓN (Treeview) ---
    
    ttk.Label(master, text="--- Cola de Pedidos ---", 
              font=('Arial', 10, 'bold')).grid(row=4, column=0, columnspan=2, pady=(10, 0))
    
    TREE_COLA = ttk.Treeview(master, columns=("Artista", "Oyente"), show="tree headings", height=10)
    TREE_COLA.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

    TREE_COLA.heading("#0", text="Canción")
    TREE_COLA.heading("Artista", text="Intérprete")
    TREE_COLA.heading("Oyente", text="Oyente")
    
    TREE_COLA.column("#0", width=250, anchor="w")
    TREE_COLA.column("Artista", width=120, anchor="center")
    TREE_COLA.column("Oyente", width=120, anchor="center")
    
    # BOTÓN PARA CANCELAR EL ÚLTIMO PEDIDO REALIZADO (UNDO)
    ttk.Button(master, 
               text="Cancelar Último Pedido ↩️", 
               command=cancelar_ultimo_pedido,
               style='Danger.TButton'
               ).grid(row=6, column=0, columnspan=2, pady=5)
    
    # Inicialización visual
    cargar_y_mostrar_imagen(RUTA_IMAGEN_POR_DEFECTO, LABEL_CARATULA, TAMANO_PREVISUALIZACION)
    ENTRY_OYENTE.focus()


ROOT = tk.Tk()
    
# Configuración de estilo
style = ttk.Style(ROOT)
style.configure('Danger.TButton', foreground='black', background='#dc3545', font=('Arial', 10, 'bold'))
style.map('Danger.TButton', background=[('active', '#c82333')])
        
crear_interfaz_principal(ROOT)
ROOT.mainloop()
