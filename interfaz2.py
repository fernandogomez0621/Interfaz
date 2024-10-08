import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk  # Necesario instalar Pillow para manejar imágenes

# Variable global para almacenar los datos
data = None

# Crear la ventana principal
root = tk.Tk()
root.title("Software de Laboratorio - Leer y Procesar Datos")
root.geometry("1000x600")
root.config(bg="white")


def cargar_archivo():
    global data
    archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", ".csv"), ("Archivos TXT", ".txt"), ("Archivos Excel", "*.xlsx *.xls")])
    
    if archivo:
        try:
            progreso.start()
            if archivo.endswith('.csv'):
                data = pd.read_csv(archivo)
            elif archivo.endswith('.txt'):
                data = pd.read_csv(archivo, delimiter='\t')
            else:
                data = pd.read_excel(archivo)
            progreso.stop()
            mostrar_datos(data)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo. Detalles: {e}")
            progreso.stop()


def mostrar_datos(datos):
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("Datos Cargados")
    nueva_ventana.geometry("800x400")

    frame_tabla = ttk.Frame(nueva_ventana)
    frame_tabla.pack(fill=tk.BOTH, expand=True)

    scrollbar_y = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL)
    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

    scrollbar_x = ttk.Scrollbar(frame_tabla, orient=tk.HORIZONTAL)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

    columnas = list(datos.columns)
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings', yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    scrollbar_y.config(command=tabla.yview)
    scrollbar_x.config(command=tabla.xview)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    for _, fila in datos.iterrows():
        tabla.insert('', tk.END, values=list(fila))

    tabla.pack(fill=tk.BOTH, expand=True)


def eliminar_nulos():
    global data
    if data is not None:
        data.dropna(inplace=True)
        messagebox.showinfo("Éxito", "Se han eliminado las filas con valores nulos")
    else:
        messagebox.showwarning("Advertencia", "Primero debes cargar los datos")


def eliminar_duplicados():
    global data
    if data is not None:
        data.drop_duplicates(inplace=True)
        messagebox.showinfo("Éxito", "Se han eliminado las filas duplicadas")
    else:
        messagebox.showwarning("Advertencia", "Primero debes cargar los datos")


def normalizar_datos():
    global data
    if data is not None:
        for col in data.select_dtypes(include='number').columns:
            data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
        messagebox.showinfo("Éxito", "Datos normalizados correctamente")
    else:
        messagebox.showwarning("Advertencia", "Primero debes cargar los datos")


def rellenar_nulos_con_media():
    global data
    if data is not None:
        data.fillna(data.mean(), inplace=True)
        messagebox.showinfo("Éxito", "Valores nulos rellenados con la media")
    else:
        messagebox.showwarning("Advertencia", "Primero debes cargar los datos")


def mostrar_leer_datos():
    limpiar_contenido()
    lbl = tk.Label(contenido_frame, text="Módulo: Leer Datos", font=("Helvetica", 16), bg="white")
    lbl.pack(pady=20)
    btn_leer_datos = tk.Button(contenido_frame, text="Seleccionar Archivo (CSV, TXT, Excel)", command=cargar_archivo, width=30, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    btn_leer_datos.pack(pady=10)


def mostrar_procesar_datos():
    limpiar_contenido()
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


def mostrar_regresiones():
    limpiar_contenido()
    lbl = tk.Label(contenido_frame, text="Módulo: Regresiones", font=("Helvetica", 16), bg="white")
    lbl.pack(pady=20)

    btn_regresion_lineal = tk.Button(contenido_frame, text="Regresión Lineal", command=lambda: messagebox.showinfo("Regresión Lineal", "Función de regresión lineal aquí."), width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
    btn_regresion_lineal.pack(pady=5)

    btn_regresion_polinomica = tk.Button(contenido_frame, text="Regresión Polinómica de Grado n", command=lambda: messagebox.showinfo("Regresión Polinómica", "Función de regresión polinómica aquí."), width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
    btn_regresion_polinomica.pack(pady=5)

    btn_interpolacion = tk.Button(contenido_frame, text="Interpolación", command=lambda: messagebox.showinfo("Interpolación", "Función de interpolación aquí."), width=25, font=("Helvetica", 12), bg="#FF5722", fg="white")
    btn_interpolacion.pack(pady=5)


def limpiar_contenido():
    for widget in contenido_frame.winfo_children():
        widget.destroy()


def mostrar_bienvenida():
    bienvenida = tk.Toplevel(root)
    bienvenida.title("Bienvenido")
    bienvenida.geometry("600x400")
    bienvenida.config(bg="white")

    lbl_bienvenida = tk.Label(bienvenida, text="¡Bienvenido al Software de Laboratorio!", font=("Helvetica", 20), bg="white")
    lbl_bienvenida.pack(pady=50)

    btn_continuar = tk.Button(bienvenida, text="Continuar", command=lambda: [bienvenida.destroy(), root.deiconify()], width=15, font=("Helvetica", 14), bg="#4CAF50", fg="white")
    btn_continuar.pack(pady=20)

    root.withdraw()


# Crear un Frame para el menú lateral
menu_frame = tk.Frame(root, width=200, bg="lightgray")
menu_frame.pack(side="left", fill="y")

# Crear un Frame para el contenido principal
contenido_frame = tk.Frame(root, bg="white")
contenido_frame.pack(side="right", expand=True, fill="both")

# Agregar botones al menú lateral
btn_menu_leer = tk.Button(menu_frame, text="Leer Datos", command=mostrar_leer_datos, width=20, font=("Helvetica", 12), bg="#2196F3", fg="white")
btn_menu_leer.pack(pady=10)

btn_menu_procesar = tk.Button(menu_frame, text="Procesar Datos", command=mostrar_procesar_datos, width=20, font=("Helvetica", 12), bg="#2196F3", fg="white")
btn_menu_procesar.pack(pady=10)

btn_menu_regresiones = tk.Button(menu_frame, text="Regresiones", command=mostrar_regresiones, width=20, font=("Helvetica", 12), bg="#2196F3", fg="white")
btn_menu_regresiones.pack(pady=10)

# Barra de progreso
progreso = Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
progreso.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

# Mostrar la pantalla de bienvenida
mostrar_bienvenida()

# Ejecutar la ventana
root.mainloop()
