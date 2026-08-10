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
    <h3 style="margin-top:0;">Datos de la autora</h3>
    <ul style="line-height:1.6; padding-left:18px;">
      <li><strong>Nombre completo:</strong> Mónica Tahiz Rantes García</li>
      <li><strong>Curso:</strong> Especialización en Python For Analytics</li>
      <li><strong>Año:</strong> 2026</li>
    </ul>
    </section>

    <section style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:15px; margin-top:12px;">
    <h3 style="margin-top:0;">Objetivo del análisis</h3>
    <p>
      Aplicar de forma integral los conceptos vistos a lo largo del curso, orientando el proyecto al Análisis Exploratorio de Datos (EDA) 
      del dataset BankMarketing.csv considerando los datos de la última campaña; ello para descubrir relaciones y comportamientos relevantes 
      entre las variables. 
    </p>
    </section>

     <section style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:20px; margin-top:12px;">
    <h3 style="margin-top:0;">Breve explicación del dataset</h3>
    <p>
      El archivo input BankMarketing.csv, corresponde a una institución financiera que busca entender los factores que influyen en la aceptación 
      de sus campañas de marketing. Durante los últimos 6 meses, la efectividad (e = (Ventas/Base)×100%) cayó de 12% a 8%, afectando los bonos de 
      los ejecutivos comerciales.
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

