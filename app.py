import streamlit as st
import numpy as np
import pandas as pd

import importlib.util 
from io import BytesIO

from textwrap import dedent


st.set_page_config(page_title="Proyecto Final- Caso Nro. 1", layout="centered")
st.title("Proyecto Final - Caso de estudio #1")
st.sidebar.title("Menú")


# *********************************************
# FUNCIONES
# *********************************************

def load_data_from_bytes(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(BytesIO(file_bytes), sep=';')

    
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
    <section style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:15px; margin-top:12px;">
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

     <section style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:15px; margin-top:12px;">
    <h3 style="margin-top:0;">Breve explicación del dataset</h3>
    <p>
      El archivo input BankMarketing.csv, corresponde a una institución financiera que busca entender los factores que influyen en la aceptación 
      de sus campañas de marketing. Durante los últimos 6 meses, la efectividad (e = (Ventas/Base)×100%) cayó de 12% a 8%, afectando los bonos de 
      los ejecutivos comerciales.
    </p>
    </section>

    <section style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:15px; margin-top:12px;">
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
    
else:
# *********************************************
# CARGA DEL DATASET
# *********************************************    
# -----------------------------------------------------------------------------
# Carga del archivo
# -----------------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### Panel de segmentación")
        st.markdown(
            '<div class="filter-caption">Los gráficos y KPIs responden a todos los filtros seleccionados.</div>',
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Fuente de datos",
            type=["csv"],
            help="Puede cargar otra versión del dataset con la misma estructura.",
        )
    
    try:
        if uploaded_file is not None:
            raw_data = load_data_from_bytes(uploaded_file.getvalue())
            source_name = uploaded_file.name
            
            # Mostrar la vista previa en la app
            st.subheader(f"Vista previa: {source_name}")
            st.dataframe(raw_data.head())
            st.success(f"Dimensiones del dataset (filas, columnas) =  **{raw_data.shape}**")
        
        else:
            st.info("Cargue el archivo CSV desde el panel lateral para iniciar el análisis.")
            st.stop()
    except Exception as exc:
        st.error(f"No fue posible leer el archivo CSV: {exc}")
        st.stop()
    
    


    

