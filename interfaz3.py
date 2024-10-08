import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, StringVar
import pandas as pd
from tkinter import ttk
from tkinter.ttk import Progressbar
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

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

def limpiar_contenido():
    for widget in contenido_frame.winfo_children():
        widget.destroy()

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

    global var_x, var_y
    var_x = StringVar()
    var_y = StringVar()

    # Crear el menú desplegable para seleccionar la variable independiente (X)
    lbl_x = tk.Label(contenido_frame, text="Selecciona variable independiente (X):", bg="white")
    lbl_x.pack(pady=5)
    opciones_x = ttk.Combobox(contenido_frame, textvariable=var_x)
    opciones_x['values'] = list(data.columns) if data is not None else []
    opciones_x.pack(pady=5)

    # Crear el menú desplegable para seleccionar la variable dependiente (Y)
    lbl_y = tk.Label(contenido_frame, text="Selecciona variable dependiente (Y):", bg="white")
    lbl_y.pack(pady=5)
    opciones_y = ttk.Combobox(contenido_frame, textvariable=var_y)
    opciones_y['values'] = list(data.columns) if data is not None else []
    opciones_y.pack(pady=5)

    btn_reg_lineal = tk.Button(contenido_frame, text="Regresión Lineal", command=regresion_lineal, width=25, font=("Helvetica", 12), bg="#FF9800", fg="white")
    btn_reg_lineal.pack(pady=5)

    btn_reg_polinomica = tk.Button(contenido_frame, text="Regresión Polinómica", command=regresion_polinomica, width=25, font=("Helvetica", 12), bg="#FF9800", fg="white")
    btn_reg_polinomica.pack(pady=5)

    btn_interpolacion = tk.Button(contenido_frame, text="Interpolación", command=interpolacion, width=25, font=("Helvetica", 12), bg="#FF9800", fg="white")
    btn_interpolacion.pack(pady=5)

def calcular_metricas(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    return r2, mae, mse

def mostrar_metricas(r2, mae, mse):
    metrics_window = tk.Toplevel()
    metrics_window.title("Métricas de Regresión")
    
    lbl_r2 = tk.Label(metrics_window, text=f"R²: {r2:.4f}", font=("Helvetica", 14))
    lbl_r2.pack(pady=5)

    lbl_mae = tk.Label(metrics_window, text=f"MAE: {mae:.4f}", font=("Helvetica", 14))
    lbl_mae.pack(pady=5)

    lbl_mse = tk.Label(metrics_window, text=f"MSE: {mse:.4f}", font=("Helvetica", 14))
    lbl_mse.pack(pady=5)

def regresion_lineal():
    global data
    if data is not None and var_x.get() and var_y.get():
        x = data[var_x.get()]
        y = data[var_y.get()]
        coef = np.polyfit(x, y, 1)  # Coeficientes de la regresión lineal
        poly_eq = np.poly1d(coef)

        y_pred = poly_eq(x)  # Predicciones

        plt.scatter(x, y, color='blue', label='Datos')
        plt.plot(x, y_pred, color='red', label='Regresión Lineal')
        plt.xlabel(var_x.get())
        plt.ylabel(var_y.get())
        plt.title("Regresión Lineal")
        plt.legend()
        plt.show()

        r2, mae, mse = calcular_metricas(y, y_pred)
        mostrar_metricas(r2, mae, mse)
    else:
        messagebox.showwarning("Advertencia", "Selecciona las variables para la regresión")

def regresion_polinomica():
    global data
    if data is not None and var_x.get() and var_y.get():
        # Solicitar el grado del polinomio
        grado = simpledialog.askinteger("Grado del Polinomio", "Ingresa el grado del polinomio:", minvalue=1, maxvalue=10)
        
        if grado is not None:
            x = data[var_x.get()]
            y = data[var_y.get()]
            coef = np.polyfit(x, y, grado)  # Coeficientes de la regresión polinómica
            poly_eq = np.poly1d(coef)

            # Generar valores de x para el modelo ajustado
            x_fit = np.linspace(x.min(), x.max(), 100)  # 100 puntos para una línea suave
            y_fit = poly_eq(x_fit)  # Predicciones

            plt.scatter(x, y, color='blue', label='Datos')
            plt.plot(x_fit, y_fit, color='red', label=f'Regresión Polinómica de grado {grado}')
            plt.xlabel(var_x.get())
            plt.ylabel(var_y.get())
            plt.title("Regresión Polinómica")
            plt.legend()
            plt.show()

            r2, mae, mse = calcular_metricas(y, poly_eq(x))  # Usar los valores de x originales para las métricas
            mostrar_metricas(r2, mae, mse)
    else:
        messagebox.showwarning("Advertencia", "Selecciona las variables para la regresión")

def interpolacion():
    global data
    if data is not None and var_x.get() and var_y.get():
        x = data[var_x.get()]
        y = data[var_y.get()]
        interp_func = interp1d(x, y, kind='linear', fill_value="extrapolate")

        x_new = np.linspace(x.min(), x.max(), 100)
        y_new = interp_func(x_new)

        plt.scatter(x, y, color='blue', label='Datos')
        plt.plot(x_new, y_new, color='green', label='Interpolación Lineal')
        plt.xlabel(var_x.get())
        plt.ylabel(var_y.get())
        plt.title("Interpolación de Datos")
        plt.legend()
        plt.show()
    else:
        messagebox.showwarning("Advertencia", "Selecciona las variables para la interpolación")

# Crear marco de contenido
contenido_frame = tk.Frame(root, bg="white")
contenido_frame.pack(fill=tk.BOTH, expand=True)

# Crear barra de progreso
progreso = Progressbar(root, orient="horizontal", mode="indeterminate")
progreso.pack(fill=tk.X)

# Crear menú principal
menu_principal = tk.Menu(root)
root.config(menu=menu_principal)

menu_principal.add_command(label="Leer Datos", command=mostrar_leer_datos)
menu_principal.add_command(label="Procesar Datos", command=mostrar_procesar_datos)
menu_principal.add_command(label="Regresiones", command=mostrar_regresiones)

# Iniciar la aplicación
root.mainloop()
