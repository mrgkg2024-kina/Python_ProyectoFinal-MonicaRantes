import streamlit as st
import numpy as np
import pandas as pd
import io

import importlib.util 
from io import BytesIO

from textwrap import dedent

st.set_page_config(
    page_title="Proyecto Final - Caso Nro. 1",
    page_icon="📊",
    layout="wide",                    # usa todo el ancho de la ventana
    initial_sidebar_state="expanded"  # "auto", "expanded" o "collapsed"
)

st.markdown('<h1 style="text-align:center;">Proyecto Final - Caso Nro. 1</h1>', unsafe_allow_html=True)
st.sidebar.title("Menú")


# *********************************************
# FUNCIONES
# *********************************************

def load_data_from_bytes(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_csv(BytesIO(file_bytes), sep=';')

def segmento_marital(df2: pd.DataFrame, column: str, estado:str) -> int:
  counts = df2['marital'].value_counts(dropna=False)
  if estado=="single":
     return int(counts.get('single', 0))
  elif estado=="married":
    return int(counts.get('married', 0))
  elif estado=="divorced":
    return int(counts.get('divorced', 0))
  else:
    return int(counts.get('unknown', 0))

    
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

    <section style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:20px; margin-top:12px;">
    <h3 style="margin-top:0;">Objetivo del análisis</h3>
    <p>
      Aplicar de forma integral los conceptos vistos a lo largo del curso, orientando el proyecto al Análisis Exploratorio de Datos (EDA) del dataset 
      BankMarketing.csv considerando los datos de la última campaña; ello para descubrir relaciones y comportamientos relevantes entre las variables. 
    </p>
    </section>

     <section style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:20px; margin-top:12px;">
    <h3 style="margin-top:0;">Breve explicación del dataset</h3>
    <p>
      El archivo input BankMarketing.csv, corresponde a una institución financiera que busca entender los factores que influyen en la aceptación de 
      sus campañas de marketing. Durante los últimos 6 meses, la efectividad (e = (Ventas/Base)×100%) cayó de 12% a 8%, afectando los bonos de los 
      ejecutivos comerciales.
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
            st.subheader(f"Vista previa del dataset: {source_name}")
            st.dataframe(raw_data.head())
            st.success(f"Dimensiones del dataset (filas, columnas) =  **{raw_data.shape}**")
        
        else:
            st.info("Cargue el archivo CSV desde el panel lateral para iniciar el análisis.")
            st.stop()
    except Exception as exc:
        st.error(f"No fue posible leer el archivo CSV: {exc}")
        st.stop()

    df = raw_data.copy()

# -----------------------------------------------------------------------------
# Navegación mediante Tabs 
# -----------------------------------------------------------------------------
    tabs = st.tabs(
        [
            "Item 1",
            "Item 2",
            "3. Estadísticas descriptivas",
            "4. Análisis de valores faltantes",
            "5. Distribución de variables numéricas", 
            "6. Análisis de variables categóricas",
            "7. Análisis bivariado (numérico vs categórico)",
            "8. Análisis bivariado (categórico vs categórico)",
            "9: Análisis basado en parámetros seleccionados",
            "10:  Hallazgos clave"
        ]
    )

# -----------------------------------------------------------------------------
# Item 1 - Información general del dataset
# -----------------------------------------------------------------------------
    
    with tabs[0]:
        st.markdown('<h2 style="text-align:center;">Información general del dataset</h2>', unsafe_allow_html=True)
        st.write("Se muestra la información general, considerando los tipos de datos y el conteo de valores nulos.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p style="color:#2b8cbe; font-weight:bold; text-align:center; font-size:18px;"> .info()</p>', unsafe_allow_html=True)
            buf = io.StringIO()
            df.info(buf=buf)
            s = buf.getvalue()
            st.markdown(f"```text\n{s}\n```")  # o st.text(s) / st.markdown(f"```text\n{s}\n```")
        with col2:
            st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:center; font-size:18px;"> Conteo de valores nulos</p>', unsafe_allow_html=True)
            #st.dataframe(df.isna().sum().to_frame("null_count"), width=350,height=600)          
            s = df.isna().sum().to_frame("null_count").reset_index().rename(columns={"index":"column"})
            styler = (s.style
                        .set_properties(subset=["column"], **{"width":"220px", "text-align":"left"})
                        .set_properties(subset=["null_count"], **{"width":"80px", "text-align":"center"})
                        .set_table_styles([
                            {"selector": "th", "props": [("text-align", "center")]}
                        ])
                    )
            st.dataframe(styler)  # o st.write(styler)

# -----------------------------------------------------------------------------
# Item 2 - Clasificación de variables
# ----------------------------------------------------------------------------- 
    with tabs[1]:
        st.markdown('<h2 style="text-align:center;">Clasificación de variables</h2>', unsafe_allow_html=True)
        st.write("""Se visualizan las variables numéricas y categóricas, así como el total de registros de la columna **marital**, clasificada por tipo,
        para lo cual se utiliza la función personalizada **segmento_marital**. También se puede elegir visualizar los totales de todos los tipos registrados
        en la columna **marital**.  \n """)
        columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()
        columnas_categoricas = df.select_dtypes(include=["object", "category", "string"]).columns.tolist()
        col1, col2,col3 = st.columns(3)
        with col1:
            st.markdown('<p style="color:#2b8cbe; font-weight:bold; text-align:center; font-size:18px;"> Variebles Numéricas</p>', unsafe_allow_html=True)
            st.write(columnas_numericas)
        with col2:
            st.markdown('<p style="color:#2b8cbe; font-weight:bold; text-align:center; font-size:18px;"> Variebles Categóricas</p>', unsafe_allow_html=True)
            st.write(columnas_categoricas)
        with col3:
            st.session_state.setdefault("clear_inputs", False)
            
            if st.session_state.clear_inputs:
                st.session_state["estado_marital_key"] = "" 
                st.session_state.clear_inputs = False

            estado_marital = st.selectbox("Columna *marital:", ["single", "married", "divorced", "unknown"], key="estado_marital_key")
            total_registros = segmento_marital(df,"marital",estado_marital)
            if st.button("Totales según selección"):
                st.write(f" Total de registros tipo **{estado_marital}**: *{total_registros}*")
                st.session_state.clear_inputs = True
            if st.button("Totales - Vista general"):
                st.dataframe(df['marital'].value_counts(dropna=False), width=200)
                 
                 

# -----------------------------------------------------------------------------
# Item 3 - Estadísticas descriptivas
# ----------------------------------------------------------------------------- 


# -----------------------------------------------------------------------------
# Item 4 - Análisis de valores faltantes
# ----------------------------------------------------------------------------- 
