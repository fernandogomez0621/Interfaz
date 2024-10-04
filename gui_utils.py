
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Treeview, Scrollbar
from data_processing import cargar_archivo, eliminar_nulos, eliminar_duplicados, normalizar_datos, rellenar_nulos_con_media

def mostrar_bienvenida(root):
    bienvenida = tk.Toplevel(root)
    bienvenida.title("Bienvenido")
    bienvenida.geometry("600x400")
    bienvenida.config(bg="white")

    lbl_bienvenida = tk.Label(bienvenida, text="¡Bienvenido al Software de Laboratorio!", font=("Helvetica", 20), bg="white")
    lbl_bienvenida.pack(pady=50)

    btn_continuar = tk.Button(bienvenida, text="Continuar", command=lambda: [bienvenida.destroy(), root.deiconify()], width=15, font=("Helvetica", 14), bg="#4CAF50", fg="white")
    btn_continuar.pack(pady=20)

    root.withdraw()


def mostrar_datos(datos):
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("Datos Cargados")
    nueva_ventana.geometry("800x400")

    frame_tabla = tk.Frame(nueva_ventana)
    frame_tabla.pack(fill=tk.BOTH, expand=True)

    scrollbar_y = Scrollbar(frame_tabla, orient=tk.VERTICAL)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    scrollbar_x = Scrollbar(frame_tabla, orient=tk.HORIZONTAL)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

    columnas = list(datos.columns)
    tabla = Treeview(frame_tabla, columns=columnas, show='headings', yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    scrollbar_y.config(command=tabla.yview)
    scrollbar_x.config(command=tabla.xview)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    for _, fila in datos.iterrows():
        tabla.insert('', tk.END, values=list(fila))

    tabla.pack(fill=tk.BOTH, expand=True)


def mostrar_leer_datos(contenido_frame):
    limpiar_contenido(contenido_frame)
    lbl = tk.Label(contenido_frame, text="Módulo: Leer Datos", font=("Helvetica", 16), bg="white")
    lbl.pack(pady=20)
    btn_leer_datos = tk.Button(contenido_frame, text="Seleccionar Archivo (CSV, TXT, Excel)", command=lambda: cargar_archivo(filedialog, None, mostrar_datos), width=30, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    btn_leer_datos.pack(pady=10)


def mostrar_procesar_datos(contenido_frame):
    limpiar_contenido(contenido_frame)
    lbl = tk.Label(contenido_frame, text="Módulo: Procesar Datos", font=("Helvetica", 16), bg="white")
    lbl.pack(pady=20)

    btn_eliminar_nulos = tk.Button(contenido_frame, text="Eliminar Nulos", command=eliminar_nulos, width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
    btn_eliminar_nulos.pack(pady=5)

    btn_eliminar_duplicados = tk.Button(contenido_frame, text="Eliminar Duplicados", command=eliminar_duplicados, width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
    btn_eliminar_duplicados.pack(pady=5)

    btn_normalizar = tk.Button(contenido_frame, text="Normalizar Datos", command=normalizar_datos, width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
    btn_normalizar.pack(pady=5)

    btn_rellenar_nulos = tk.Button(contenido_frame, text="Rellenar Nulos con Media", command=rellenar_nulos_con_media, width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
    btn_rellenar_nulos.pack(pady=5)


def limpiar_contenido(contenido_frame):
    for widget in contenido_frame.winfo_children():
        widget.destroy()
