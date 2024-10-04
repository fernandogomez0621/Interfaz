
import tkinter as tk

def limpiar_contenido(frame):
    for widget in frame.winfo_children():
        widget.destroy()

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
