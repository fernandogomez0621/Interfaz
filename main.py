import streamlit as st
import os

# Título de la aplicación
st.title("Mostrar y Agregar Código C++ en Streamlit")

# Nombre del archivo donde se guardará el código
codigo_file = "codigo_agrupado.cpp"

# Función para cargar códigos desde el archivo
def cargar_codigos():
    if os.path.exists(codigo_file):
        with open(codigo_file, "r") as f:
            return f.read()
    return ""

# Función para guardar códigos en el archivo
def guardar_codigo(codigo):
    with open(codigo_file, "a") as f:
        f.write(codigo + "\n\n")  # Agrega doble nueva línea para separar bloques

# Cargar códigos existentes
codigo_almacenado = cargar_codigos()

# Input para subir nuevo código C++
nuevo_codigo = st.text_area("Ingresa tu código C++ aquí:")

if st.button("Agregar Código"):
    if nuevo_codigo:
        guardar_codigo(nuevo_codigo)
        st.success("Código agregado exitosamente!")
        codigo_almacenado = cargar_codigos()  # Actualizar el contenido mostrado
    else:
        st.warning("Por favor, ingresa algún código.")

# Mostrar todo el código C++ almacenado
st.subheader("Código C++ almacenado:")
st.code(codigo_almacenado.strip(), language='cpp')

st.text("Compilación: g++ -I Eigen/ codigo_agrupado.cpp")
st.text("https://www.dmae.upct.es/~paredes/calcnum/apuntes/apuntes_tema_2.pdf")
st.text("https://www.ugr.es/~mpasadas/ftp/Tema3.pdf")
st.text("https://www.ingenieria.unam.mx/pinilla/PE105117/pdfs/tema3/3-3_metodos_jacobi_gauss-seidel.pdf")
st.text("Kevin es MKA")
