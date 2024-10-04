
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
    """
    Abre un diálogo para seleccionar un archivo CSV, TXT o Excel y carga los datos en una variable global.
    
    Esta función permite al usuario seleccionar un archivo de diferentes formatos (CSV, TXT o Excel),
    cargarlo y mostrar los datos en una nueva ventana.

    :raises: Muestra un mensaje de error en caso de que no se pueda cargar el archivo.
    """
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
    """
    Muestra los datos cargados en una nueva ventana.

    Esta función crea una nueva ventana con un `Treeview` que contiene los datos cargados.
    También agrega barras de desplazamiento horizontales y verticales si el contenido sobrepasa
    el tamaño de la ventana.

    :param datos: Un DataFrame de Pandas que contiene los datos que se van a mostrar.
    """
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
    """
    Elimina filas con valores nulos del DataFrame cargado.

    Esta función elimina todas las filas que contengan valores nulos en el DataFrame global `data`.
    Muestra un mensaje de éxito al completar la operación, o un mensaje de advertencia si no hay datos cargados.
    """
    global data
    if data is not None:
        data.dropna(inplace=True)
        messagebox.showinfo("Éxito", "Se han eliminado las filas con valores nulos")
    else:
        messagebox.showwarning("Advertencia", "Primero debes cargar los datos")


def eliminar_duplicados():
    """
    Elimina filas duplicadas del DataFrame cargado.

    Esta función elimina todas las filas duplicadas en el DataFrame global `data`.
    Muestra un mensaje de éxito al completar la operación, o un mensaje de advertencia si no hay datos cargados.
    """
    global data
    if data is not None:
        data.drop_duplicates(inplace=True)
        messagebox.showinfo("Éxito", "Se han eliminado las filas duplicadas")
    else:
        messagebox.showwarning("Advertencia", "Primero debes cargar los datos")


def normalizar_datos():
    """
    Normaliza los datos numéricos del DataFrame.

    Esta función normaliza todas las columnas numéricas en el DataFrame global `data` entre 0 y 1.
    Muestra un mensaje de éxito al completar la operación, o un mensaje de advertencia si no hay datos cargados.
    """
    global data
    if data is not None:
        for col in data.select_dtypes(include='number').columns:
            data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())
        messagebox.showinfo("Éxito", "Datos normalizados correctamente")
    else:
        messagebox.showwarning("Advertencia", "Primero debes cargar los datos")


def rellenar_nulos_con_media():
    """
    Rellena los valores nulos con la media de cada columna numérica.

    Esta función rellena los valores nulos de todas las columnas numéricas en el DataFrame global `data`
    con la media de cada columna. Muestra un mensaje de éxito al completar la operación, o un mensaje de advertencia si no hay datos cargados.
    """
    global data
    if data is not None:
        data.fillna(data.mean(), inplace=True)
        messagebox.showinfo("Éxito", "Valores nulos rellenados con la media")
    else:
        messagebox.showwarning("Advertencia", "Primero debes cargar los datos")


def mostrar_leer_datos():
    """
    Cambia la interfaz para permitir la selección y carga de un archivo.

    Esta función limpia el contenido actual del frame y agrega los elementos necesarios
    para que el usuario pueda seleccionar un archivo y cargarlo.
    """
    limpiar_contenido()
    lbl = tk.Label(contenido_frame, text="Módulo: Leer Datos", font=("Helvetica", 16), bg="white")
    lbl.pack(pady=20)
    btn_leer_datos = tk.Button(contenido_frame, text="Seleccionar Archivo (CSV, TXT, Excel)", command=cargar_archivo, width=30, font=("Helvetica", 12), bg="#4CAF50", fg="white")
    btn_leer_datos.pack(pady=10)


def mostrar_procesar_datos():
    """
    Cambia la interfaz para mostrar las opciones de procesamiento de datos.

    Esta función limpia el contenido actual del frame y agrega botones para las diferentes
    funciones de procesamiento de datos, como eliminar nulos, eliminar duplicados y normalizar datos.
    """
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


def limpiar_contenido():
    """
    Limpia todo el contenido del frame actual.

    Esta función elimina todos los widgets que están actualmente en el frame para permitir la
    adición de nuevos elementos.
    """
    for widget in contenido_frame.winfo_children():
        widget.destroy()


def mostrar_bienvenida():
    """
    Muestra una ventana de bienvenida al iniciar la aplicación.

    Esta función muestra una ventana emergente con un mensaje de bienvenida y un botón
    para continuar a la aplicación principal.
    """
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

# Barra de progreso
progreso = Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
progreso.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

# Mostrar la pantalla de bienvenida
mostrar_bienvenida()

# Iniciar la ventana principal
root.mainloop()
