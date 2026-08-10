import streamlit as st
import numpy as np
from textwrap import dedent


st.set_page_config(page_title="Proyecto Final- Caso Nro. 1", layout="centered")
st.title("Proyecto Final - Caso de estudio #1")
st.sidebar.title("Menú")

# *********************************************
# NAVEGACIÓN ENTRE LAS OPCIONES DEL MENU
# *********************************************

# Creamos un selectbox en la barra lateral.

modulo = st.sidebar.selectbox("Elija un módulo", ["Home","Carga del dataset"])

# *********************************************
# HOME
# *********************************************

if modulo == "Home":
    home_html = dedent("""
    <section style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:20px; margin-top:12px;">
    <h3 style="margin-top:0;">Datos del proyecto</h3>
    <ul style="line-height:1.6; padding-left:18px;">
      <li><strong>Nombre completo del estudiante:</strong> Mónica Tahiz Rantes García</li>
      <li><strong>Nombre del módulo:</strong> Módulo 1 – Python Fundamentals</li>
      <li><strong>Año:</strong> 2026</li>
    </ul>
    </section>

    <section style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:20px; margin-top:12px;">
    <h3 style="margin-top:0;">Descripción del proyecto</h3>
    <p>
      Se desarrolla una aplicación interactiva en Streamlit que integra los conceptos fundamentales
      aprendidos durante el Módulo 1 del curso; incluyendo variables, estructuras de datos, control
      de flujo, funciones, programación funcional, programación orientada a objetos (POO) y  operaciones básicas tipo CRUD.
    </p>
    </section>

    <section style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:20px; margin-top:12px;">
    <h3 style="margin-top:0;">Tecnologías utilizadas</h3>
    <div style="display:flex; gap:8px; flex-wrap:wrap;">
      <span style="background:#f3f4f6; border:1px solid #e5e7eb; padding:6px 10px; border-radius:999px;">Python</span>
      <span style="background:#f3f4f6; border:1px solid #e5e7eb; padding:6px 10px; border-radius:999px;">Streamlit</span>
      <span style="background:#f3f4f6; border:1px solid #e5e7eb; padding:6px 10px; border-radius:999px;">NumPy</span>
      <span style="background:#f3f4f6; border:1px solid #e5e7eb; padding:6px 10px; border-radius:999px;">Pandas</span>
    </div>
    </section>
    </div>
    """)
    st.components.v1.html(home_html, height=650, scrolling=True)

