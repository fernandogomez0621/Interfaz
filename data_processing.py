
import pandas as pd
from tkinter import filedialog, messagebox

# Variable global para almacenar los datos
data = None

def cargar_archivo(progreso, contenido_frame):
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
            mostrar_datos(data, contenido_frame)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo. Detalles: {e}")
            progreso.stop()

def mostrar_datos(datos, frame):
    from tkinter import ttk, Toplevel
    nueva_ventana = Toplevel()
    nueva_ventana.title("Datos Cargados")
    nueva_ventana.geometry("800x400")

    frame_tabla = ttk.Frame(nueva_ventana)
    frame_tabla.pack(fill="both", expand=True)

    scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")

    scrollbar_x = ttk.Scrollbar(frame_tabla, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    columnas = list(datos.columns)
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings', yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    scrollbar_y.config(command=tabla.yview)
    scrollbar_x.config(command=tabla.xview)

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    for _, fila in datos.iterrows():
        tabla.insert('', 'end', values=list(fila))

    tabla.pack(fill="both", expand=True)

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
