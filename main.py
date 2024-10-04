
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import gui_utils as gui
import data_processing as dp
from tkinter import ttk

# Variable global para almacenar los datos
data = None

# Crear la ventana principal
root = tk.Tk()
root.title("Software de Laboratorio - Leer y Procesar Datos")
root.geometry("1000x600")
root.config(bg="white")

# Crear un Frame para el menú lateral
menu_frame = tk.Frame(root, width=200, bg="lightgray")
menu_frame.pack(side="left", fill="y")

# Crear un Frame para el contenido principal
contenido_frame = tk.Frame(root, bg="white")
contenido_frame.pack(side="right", expand=True, fill="both")

# Barra de progreso
progreso = Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
progreso.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

def mostrar_leer_datos():
    gui.limpiar_contenido(contenido_frame)
    lbl = tk.Label(contenido_frame, text="Módulo: Leer Datos", font=("Helvetica", 16), bg="white")
    lbl.pack(pady=20)
    btn_leer_datos = tk.Button(contenido_frame, text="Seleccionar Archivo (CSV, TXT, Excel)", 
                               command=lambda: dp.cargar_archivo(progreso, contenido_frame), width=30, font=("Helvetica", 12), 
                               bg="#4CAF50", fg="white")
    btn_leer_datos.pack(pady=10)

def mostrar_procesar_datos():
    gui.limpiar_contenido(contenido_frame)
    lbl = tk.Label(contenido_frame, text="Módulo: Procesar Datos", font=("Helvetica", 16), bg="white")
    lbl.pack(pady=20)

    btn_eliminar_nulos = tk.Button(contenido_frame, text="Eliminar Nulos", 
                                   command=dp.eliminar_nulos, width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
    btn_eliminar_nulos.pack(pady=5)

    btn_eliminar_duplicados = tk.Button(contenido_frame, text="Eliminar Duplicados", 
                                        command=dp.eliminar_duplicados, width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
    btn_eliminar_duplicados.pack(pady=5)

    btn_normalizar = tk.Button(contenido_frame, text="Normalizar Datos", 
                               command=dp.normalizar_datos, width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
    btn_normalizar.pack(pady=5)

    btn_rellenar_nulos = tk.Button(contenido_frame, text="Rellenar Nulos con Media", 
                                   command=dp.rellenar_nulos_con_media, width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
    btn_rellenar_nulos.pack(pady=5)

# Agregar botones al menú lateral
btn_menu_leer = tk.Button(menu_frame, text="Leer Datos", command=mostrar_leer_datos, width=20, font=("Helvetica", 12), bg="#2196F3", fg="white")
btn_menu_leer.pack(pady=10)

btn_menu_procesar = tk.Button(menu_frame, text="Procesar Datos", command=mostrar_procesar_datos, width=20, font=("Helvetica", 12), bg="#2196F3", fg="white")
btn_menu_procesar.pack(pady=10)

# Mostrar la pantalla de bienvenida
gui.mostrar_bienvenida(root)

# Iniciar la ventana principal
root.mainloop()
