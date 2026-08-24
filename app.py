import streamlit as st
import numpy as np
import pandas as pd

import importlib.util 
import io
from io import BytesIO
from textwrap import dedent

import matplotlib.pyplot as plt
import seaborn as sns
import itertools

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

def segmento_marital(df1: pd.DataFrame, column: str, estado:str) -> int:
  counts = df1['marital'].value_counts(dropna=False)
  if estado=="single":
     return int(counts.get('single', 0))
  elif estado=="married":
    return int(counts.get('married', 0))
  elif estado=="divorced":
    return int(counts.get('divorced', 0))
  else:
    return int(counts.get('unknown', 0))

def obtener_var_categoricas(df2:pd.Dataframe) -> list:
    return df2.select_dtypes(include=["object", "category", "string"]).columns.tolist()

def obtener_var_numericas(df3:pd.Dataframe) -> list:
    return df3.select_dtypes(include=["number"]).columns.tolist()
    

def crear_grafico_barras(df4, variable):
    # Reemplazar valores faltantes y calcular conteos
    datos = df4[variable].fillna("Valor faltante").astype(str)
    conteos = datos.value_counts()

    # Calcular proporciones
    proporciones = conteos / conteos.sum()

    # Crear tabla de frecuencias
    tabla = pd.DataFrame({
        "Categoría": conteos.index,
        "Conteo": conteos.values,
        "Proporción": proporciones.values,
        "Porcentaje": proporciones.values * 100
    })

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(6,3))

    barras = ax.bar(
        tabla["Categoría"],
        tabla["Conteo"],
        width=0.5,
        color="steelblue",
        edgecolor="black",
        linewidth=0.5
    )

    # Crear etiquetas con conteo y porcentaje
    etiquetas = [
        f"{conteo}\n({porcentaje:.1f}%)"
        for conteo, porcentaje in zip(
            tabla["Conteo"],
            tabla["Porcentaje"]
        )
    ]

   # Agregar etiquetas sobre las barras
    ax.bar_label(
        barras,
        labels=etiquetas,
        padding=2,
        fontsize=5
    )

    # Personalizar el gráfico
    ax.set_title(
        f"Distribución de la variable: {variable}",
        fontsize=7,
        fontweight="bold"
    )
    ax.set_xlabel(variable, fontsize=8)
    ax.set_ylabel("Conteo", fontsize=8)

    ax.tick_params(
        axis="x",
        rotation=45,
        labelsize=5
    )
    ax.tick_params(
        axis="y",
        labelsize=5
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    # Enviar la cuadrícula detrás de las barras
    ax.set_axisbelow(True)

    # Ocultar bordes superior y derecho
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Evitar que las etiquetas queden cortadas
    if not tabla.empty:
        ax.set_ylim(
            0,
            tabla["Conteo"].max() * 1.25
        )

    fig.tight_layout()

    return tabla, fig


    
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
            "Item 3",
            "Item 4",
            "Item 5", 
            "Item 6",
            "Item 7",
            "Item 8",
            "Item 9",
            "Item 10"
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
            st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:center; font-size:18px;"> Conteo de valores nulos</p>', 
                        unsafe_allow_html=True)
            #conteo de valores nulos     
            s = df.isna().sum().to_frame("null_count").reset_index().rename(columns={"index":"column"})
            styler = (s.style
                        .set_properties(subset=["column"], **{"width":"220px", "text-align":"left"})
                        .set_properties(subset=["null_count"], **{"width":"80px", "text-align":"center"})
                        .set_table_styles([
                            {"selector": "th", "props": [("text-align", "center")]}
                        ])
                    )
            st.dataframe(styler) 

# -----------------------------------------------------------------------------
# Item 2 - Clasificación de variables
# ----------------------------------------------------------------------------- 
    with tabs[1]:
        st.markdown('<h2 style="text-align:center;">Clasificación de variables</h2>', unsafe_allow_html=True)
        st.write("""Se visualizan las variables numéricas y categóricas, así como el total de registros de la columna **marital**, clasificada por tipo,
        para lo cual se utiliza la función personalizada **segmento_marital**. También se puede elegir visualizar los totales de todos los tipos registrados
        en la columna **marital**.  \n """)
        
        columnas_numericas = obtener_var_numericas(df)
        #columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()
        columnas_categoricas = obtener_var_categoricas(df) 
        
        col1, col2,col3 = st.columns(3)
        with col1:
            st.markdown('<p style="color:#2b8cbe; font-weight:bold; text-align:center; font-size:18px;"> Variables Numéricas</p>', unsafe_allow_html=True)
            st.write(columnas_numericas)
        with col2:
            st.markdown('<p style="color:#2b8cbe; font-weight:bold; text-align:center; font-size:18px;"> Variables Categóricas</p>', unsafe_allow_html=True)
            st.write(columnas_categoricas)
        with col3:
            st.session_state.setdefault("clear_inputs", False)
            
            if st.session_state.clear_inputs:
                st.session_state["estado_marital_key"] = "" 
                st.session_state.clear_inputs = False

            estado_marital = st.selectbox("Columna marital:", ["single", "married", "divorced", "unknown"], width=250, key="estado_marital_key")
            total_registros = segmento_marital(df,"marital",estado_marital)
            if st.button("Totales según selección"):
                st.write(f" Total de registros tipo **{estado_marital}**: *{total_registros}*")
                st.session_state.clear_inputs = True
            if st.button("Totales - Vista general"):
                st.dataframe(df['marital'].value_counts(dropna=False), width=250)
               
                 

# -----------------------------------------------------------------------------
# Item 3 - Estadísticas descriptivas
# ----------------------------------------------------------------------------- 
    with tabs[2]:
        st.markdown('<h2 style="text-align:center;">Estadísticas descriptivas</h2>', unsafe_allow_html=True)
        st.write("")    

        # columnas
        num_cols = obtener_var_numericas(df)
        cat_cols = obtener_var_categoricas(df)
        
        # Estadísticas de variables numéricas
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p style="color:#2b8cbe; font-weight:bold; text-align:center; font-size:18px;"> Estadísticas para variables numéricas</p>', 
                        unsafe_allow_html=True)
            estadisticas_num = df.describe()
            st.dataframe(estadisticas_num) 

        with col2:
           # Interpretación simple para numéricas
            num_stats = []
            for c in num_cols:
                mean = df[c].mean()
                median = df[c].median()
                std = df[c].std()
                cv = std / mean if mean not in (0, np.nan) else np.nan
                skew = "≈ simétrica" if np.isclose(mean, median, atol=1e-8) else ("asimetría derecha" if mean>median else "asimetría izquierda")
                disp = "Baja dispersión" if pd.notna(cv) and cv < 0.2 else ("Dispersión moderada" if pd.notna(cv) and cv < 0.5 else "Alta dispersión")
                num_stats.append(f"- **{c}**: media={mean:.3f}, mediana={median:.3f}, std={std:.3f} → {skew}; {disp}")
            
            st.markdown('<p style="color:#2b8cbe; font-weight:bold; text-align:center; font-size:18px;"> Interpretación — Variables numéricas</p>',
                        unsafe_allow_html=True)     
            st.markdown(f'<small style="color:#000000;">{"<br>".join(num_stats)}</small>', unsafe_allow_html=True)
        
        # Estadísticas de variables categóricas
        colA, colB = st.columns(2)
        with colA:
            st.markdown('<p style="color:#2b8cbe; font-weight:bold; text-align:center; font-size:18px;"> Estadísticas para variables categóricas</p>', 
                        unsafe_allow_html=True)
            estadisticas_cat = df.describe(include=["object"])
            st.dataframe(estadisticas_cat) 

        with colB:
             # Interpretación simple para categóricas
            cat_stats = []
            for c in cat_cols:
                vc = df[c].value_counts(dropna=False)
                top = vc.index[0]
                top_count = int(vc.iloc[0])
                total = int(vc.sum())
                pct = top_count / total * 100 if total>0 else 0
                uniques = df[c].nunique(dropna=True)
                nulls = int(df[c].isna().sum())
                cat_stats.append(f"- **{c}**: top='{top}' ({top_count} / {total}, {pct:.1f}%), únicas={uniques}, nulos={nulls}")
            
            st.markdown('<p style="color:#2b8cbe; font-weight:bold; text-align:center; font-size:18px;"> Interpretación — Variables categóricas</p>',
                        unsafe_allow_html=True)     
            st.markdown(f'<small style="color:#000000;">{"<br>".join(cat_stats)}</small>', unsafe_allow_html=True)
            
# -----------------------------------------------------------------------------
# Item 4 - Análisis de valores faltantes
# ----------------------------------------------------------------------------- 
    with tabs[3]:
        st.markdown('<h2 style="text-align:center;">Análisis de valores faltantes</h2>', unsafe_allow_html=True)
        st.write("")  

        st.markdown("""El análisis no detectó valores nulos, cadenas vacías ni celdas que contengan solo espacios en las columnas examinadas. El dataset estaría completo 
                    según estas comprobaciones.""", unsafe_allow_html=True)
        
        col1, col2,col3 = st.columns(3)
        with col1:
            st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:center; font-size:18px;"> Conteo de valores nulos</p>', 
                            unsafe_allow_html=True)
            nulos = df.isna().sum().to_frame("null_count").reset_index().rename(columns={"index":"column"})
            nulos.columns = ["column", "Conteo de nulos"]

            styler = (nulos.style
                        .set_properties(subset=["column"], **{"width":"220px", "text-align":"left"})
                        .set_properties(subset=["Conteo de nulos"], **{"width":"80px", "text-align":"center"})
                        .set_table_styles([
                        {"selector": "th", "props": [("text-align", "center")]}
                        ])
                    )
            st.dataframe(styler) 
        
        with col2:
            st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:center; font-size:18px;"> Conteo de strings vacíos por columnas</p>', 
                            unsafe_allow_html=True)
 
            empty_str_counts = df.select_dtypes(include=['object']).apply(lambda col: col.eq('').sum())

            # convertir en DataFrame y renombrar la columna
            df_empty = empty_str_counts.rename("Strings vacíos").reset_index()
            df_empty.columns = ["column", "Strings vacíos"]  # index -> column, values -> Strings vacíos

            styler2 = (df_empty.style
                       .set_properties(subset=["column"], **{"width": "220px", "text-align": "left"})
                       .set_properties(subset=["Strings vacíos"], **{"width": "80px", "text-align": "center"})
                       .set_table_styles([{"selector": "th", "props": [("text-align", "center")]}])
                      )
            st.dataframe(styler2)

        with col3:
            st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:center; font-size:18px;">Conteo de strings c/solo espacios (ejm. " ")</p>', 
                            unsafe_allow_html=True)
            spaces_only_counts = (df.select_dtypes(include=['object']).apply(lambda col: col.str.strip().eq('').sum()))

            # convertir en DataFrame y renombrar la columna
            df_spaces = spaces_only_counts.rename("Strings c/solo espacios").reset_index()
            df_spaces.columns = ["column", "Strings c/solo espacios"]  # index -> column, values -> Strings vacíos

            
            styler3 = ( df_spaces.style
                        .set_properties(subset=["column"], **{"width":"220px", "text-align":"left"})
                        .set_properties(subset=["Strings c/solo espacios"], **{"width":"80px", "text-align":"center"})
                        .set_table_styles([
                        {"selector": "th", "props": [("text-align", "center")]}
                        ])
                      )
            st.dataframe(styler3)         

# -----------------------------------------------------------------------------
# Item 5 - Distribución de variables numéricas
# ----------------------------------------------------------------------------- 
        with tabs[4]:
            st.markdown('<h2 style="text-align:center;">Distribución de variables numéricas</h2>', unsafe_allow_html=True)
            st.write("")  
            st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:left; font-size:18px;">Histogramas de las variables numéricas</p>', 
                            unsafe_allow_html=True)
            st.write("")  

            num_cols = obtener_var_numericas(df)
            sns.set(style="whitegrid")   
           
            color = "#2b8cbe"
            bins = 30  

            # Mostrar histogramas en filas de 3
            cols_per_row = 3
            for i, col in enumerate(num_cols):
                if i % cols_per_row == 0:
                    row = st.columns(cols_per_row)
                with row[i % cols_per_row]:
                    series = df[col].dropna()
                    fig, ax = plt.subplots(figsize=(4, 3))
                    # Histograma con color y borde
                    sns.histplot(series, bins=bins, kde=False, color=color, edgecolor='k', ax=ax, alpha=0.8)
                    # Líneas de media y mediana
                    ax.axvline(series.mean(), color='red', linestyle='--', linewidth=1, label='media')
                    ax.axvline(series.median(), color='green', linestyle='-.', linewidth=1, label='mediana')
                    ax.set_title(col, fontsize=11)
                    ax.set_xlabel("")
                    ax.set_ylabel("Frecuencia")
                    ax.legend(fontsize=8)
                    st.pyplot(fig)

# -----------------------------------------------------------------------------
# Item 6 - Análisis de variables categóricas
# ----------------------------------------------------------------------------- 
        with tabs[5]:
            st.markdown('<h2 style="text-align:center;">Análisis de variables categóricas</h2>', unsafe_allow_html=True)
            st.write("")  

            # Identificar variables categóricas
            variables_categoricas = obtener_var_categoricas(df)

            if variables_categoricas:
                texto_variables = " | ".join(variables_categoricas)
                st.markdown(
                    f"""
                    <div style="
                        background-color: #ffffff;
                        padding: 12px;
                        border-radius: 8px;
                        border: 2px solid #2b8cbe;
                        color: #2b8cbe;
                        text-align: center;
                    ">
                        <strong>Variables categóricas ({len(variables_categoricas)}):</strong>
                        <span>{texto_variables}</span>
                    </div>""", unsafe_allow_html=True)    
                st.write("")  
                
                # Elegir cómo mostrar los resultados
                opcion = st.radio(
                    "Selecciona una opción:",
                    [
                        "Mostrar una variable",
                        "Mostrar todas las variables"
                    ]
                )

                if opcion == "Mostrar una variable":

                    variable_seleccionada = st.selectbox("Selecciona una variable categórica:", variables_categoricas)
                    tabla, fig = crear_grafico_barras(df, variable_seleccionada)
                    st.subheader(f"Resultados de: {variable_seleccionada}")

                    # Formatear la tabla
                    st.dataframe(
                        tabla.style.format({
                            "Proporción": "{:.4f}",
                            "Porcentaje": "{:.2f}%"
                        }),
                        use_container_width=True
                    )

                    # Mostrar gráfico
                    st.pyplot(fig)
                    plt.close(fig)

                else:

                    # Mostrar todas las variables categóricas
                    for variable in variables_categoricas:
                        st.subheader(f"Variable: {variable}")
                        tabla, fig = crear_grafico_barras(df,variable)

                        st.dataframe(
                            tabla.style.format({
                                "Proporción": "{:.4f}",
                                "Porcentaje": "{:.2f}%"
                            }),
                            use_container_width=True
                        )

                        st.pyplot(fig)
                        plt.close(fig)

            else:
                st.warning("El archivo no contiene variables categóricas.")    
            
# -----------------------------------------------------------------------------
# Item 7 - Análisis bivariado (numérico vs categórico)
# ----------------------------------------------------------------------------- 
        with tabs[6]:
            st.markdown('<h2 style="text-align:center;">Análisis bivariado (numérico vs categórico)</h2>', unsafe_allow_html=True)
            st.markdown("""Para el análisis tenemos: la variable numérica **age (edad)** y la variable categórica **job (trabajo)**. Se muestra un breve análisis 
                    estadístico de ambas variables, así como el gráfico comparativo asociado. Finalmente se da una breve interpretación del gráfico.""",
                    unsafe_allow_html=True)
            st.write("")  

            # Preparar los datos
            datos = df[["age", "job"]].copy()

            # Convertir age a formato numérico
            datos["age"] = pd.to_numeric(datos["age"], errors="coerce")

            # Eliminar registros vacíos
            datos = datos.dropna(subset=["age", "job"])

            if datos.empty:
                st.warning("No existen datos válidos en las columnas age y job.")
                st.stop()

            col1, col2 = st.columns([1,2])
            with col1:
                st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:center; font-size:18px;">Resumen estadístico</p>', 
                            unsafe_allow_html=True)   
                
                # Resumen estadístico por tipo de trabajo
                resumen = (
                    datos.groupby("job")["age"]
                    .agg(
                        cantidad="count",
                        edad_promedio="mean",
                        edad_mediana="median",
                        edad_minima="min",
                        edad_maxima="max"
                    )
                    .sort_values("edad_promedio", ascending=True)
                    .round(1)
                )
                            
                st.dataframe(
                    resumen,
                    use_container_width=True
                )

            with col2:
                st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:center; font-size:18px;">Gráfico comparativo</p>', 
                            unsafe_allow_html=True)   
                # Crear gráfico horizontal
                fig, ax = plt.subplots(figsize=(9, 6))
        
                barras = ax.barh(
                    resumen.index.astype(str),
                    resumen["edad_promedio"],
                    color="#4682B4",
                    edgecolor="black",
                    linewidth=0.6
                )
    
                # Mostrar edad promedio al final de cada barra
                ax.bar_label(
                    barras,
                    labels=[
                        f"{edad:.1f} años"
                        for edad in resumen["edad_promedio"]
                    ],
                    padding=3,
                    fontsize=9
                )
    
                ax.set_title("Edad promedio de los clientes según su tipo de trabajo")
                ax.set_xlabel("Edad promedio")
                ax.set_ylabel("Tipo de trabajo")
    
                ax.grid(axis="x", linestyle="--", alpha=0.3)
    
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
    
                # Agregar espacio para las etiquetas
                edad_maxima = resumen["edad_promedio"].max()
    
                if edad_maxima > 0:
                    ax.set_xlim(0, edad_maxima * 1.20)
    
                plt.tight_layout()                             
                st.pyplot(fig, use_container_width=False)
                plt.close(fig)

            st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:left; font-size:18px;">Interpretación</p>', 
                            unsafe_allow_html=True)   
            
            trabajo_mayor = resumen["edad_promedio"].idxmax()
            promedio_mayor = resumen["edad_promedio"].max()

            trabajo_menor = resumen["edad_promedio"].idxmin()
            promedio_menor = resumen["edad_promedio"].min()

            diferencia = promedio_mayor - promedio_menor

            st.write(f"- El grupo de clientes con trabajo **{trabajo_mayor}** presenta la edad promedio más alta: **{promedio_mayor:.1f} años**.")
            st.write(f"- El grupo con trabajo **{trabajo_menor}** presenta la edad promedio más baja: **{promedio_menor:.1f} años**.")
            st.write(f"- La diferencia entre ambas edades promedio es de **{diferencia:.1f} años**.")
    
# -----------------------------------------------------------------------------
# Item 8 - Análisis bivariado (categórico vs categórico) 
# ----------------------------------------------------------------------------- 
        with tabs[7]:
            st.markdown('<h2 style="text-align:center;">Análisis bivariado (categórico vs categórico)</h2>', unsafe_allow_html=True)    
            st.markdown("""Como primera variable categórica tenemos **job (trabajo)** y como segunda variable se brinda 2 opciones: **y (respuesta a la campaña)** y 
                    **education (nivel educativo)**. Se muestra un resumen estadístico de la primera y segunda variable elegida, así como el mapa de calor. Finalmente 
                    se da una breve interpretación del gráfico.""", unsafe_allow_html=True)
            st.write("")  
  
            # ------------------------------------------
            # 2. Selección de variables
            # ------------------------------------------
            variable_1 = "job"
            st.write("Primera variable : **job**")  
            variable_2 = st.selectbox("Seleccione la segunda variable:", options=["y", "education"])

            columnas_requeridas = [variable_1, variable_2]

            # ------------------------------------------
            # 3. Preparar los datos
            # ------------------------------------------
            datos = df[[variable_1, variable_2]].dropna().copy()
            datos[variable_1] = (datos[variable_1].astype(str).str.strip().str.lower())
            datos[variable_2] = (datos[variable_2].astype(str).str.strip().str.lower())

            if datos.empty:
                st.warning("No existen registros válidos para realizar el análisis.")
                st.stop()

            st.info(f"Se analizaron **{len(datos):,} registros válidos**.")

            # ------------------------------------------
            # 4. Tablas de contingencia
            # ------------------------------------------
            tabla_frecuencias = pd.crosstab(datos[variable_1], datos[variable_2])
            tabla_frecuencias_total = pd.crosstab(datos[variable_1], datos[variable_2], margins=True, margins_name="Total")
    
            # Los porcentajes de cada fila suman 100 %
            tabla_porcentajes = pd.crosstab(datos[variable_1], datos[variable_2], normalize="index").mul(100).round(2)

            # ------------------------------------------
            # 5. Mostrar tablas
            # ------------------------------------------
            st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:center; font-size:21px;">Resumen estadístico</p>', 
                            unsafe_allow_html=True)   
              
            columna_1, columna_2 = st.columns(2)

            with columna_1:
                st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:center; font-size:18px;">Tabla de frecuencias</p>', 
                            unsafe_allow_html=True)   
                st.dataframe(tabla_frecuencias_total, use_container_width=True)

            with columna_2:
                st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:center; font-size:18px;">Tabla de porcentajes por trabajo</p>', 
                            unsafe_allow_html=True)   
                #st.caption("Cada fila representa un trabajo y suma 100 %.")
    
                # Agregar el símbolo % para presentación
                tabla_porcentajes_mostrar = (tabla_porcentajes.astype(str) + " %")
    
                st.dataframe(tabla_porcentajes_mostrar, use_container_width=True)

            # ------------------------------------------
            # 6. Mapa de calor
            # ------------------------------------------
            st.write("")  
            st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:center; font-size:21px;">Mapa de calor</p>', 
                            unsafe_allow_html=True)   
               
            if variable_2 == "y":
                titulo = "Respuesta a la campaña según el tipo de trabajo"
                etiqueta_x = "Respuesta a la campaña"
            else:
                titulo = "Nivel educativo según el tipo de trabajo"
                etiqueta_x = "Nivel educativo"
    
            sns.set_theme(style="white")
            alto = max(3.5, len(tabla_porcentajes.index) * 0.38)
            fig, ax = plt.subplots(figsize=(6.5, alto))

            sns.heatmap(
                tabla_porcentajes,
                annot=True,
                annot_kws={"fontsize": 7}, 
                fmt=".1f",
                cmap="YlGnBu",
                linewidths=0.4,
                linecolor="white",
                cbar_kws={"label": "Porcentaje (%)","shrink": 0.75 },
                ax=ax
            )

            ax.set_title(
                titulo,
                fontsize=9,
                fontweight="bold",
                pad=8
            )

            ax.set_xlabel(etiqueta_x, fontsize=8, labelpad=5)
            ax.set_ylabel("Tipo de trabajo", fontsize=8, labelpad=5)
    
            ax.tick_params(axis="x", labelsize=7, rotation=45)
            ax.tick_params(axis="y", labelsize=7, rotation=0)
    
            plt.tight_layout()
    
            st.pyplot(fig, use_container_width=False)
            plt.close(fig)

            # ------------------------------------------
            # 7. Interpretación automática
            # ------------------------------------------
            st.write("")  
            st.markdown('<p style="color:#2b8cbe; font-weight:bold ; text-align:center; font-size:21px;">Interpretación</p>', 
                            unsafe_allow_html=True)   
            #st.subheader("Interpretación automática")
    
            if variable_2 == "y":
                # Verificar que exista la categoría "yes"
                if "yes" in tabla_porcentajes.columns:
       
                    porcentajes_yes = tabla_porcentajes["yes"]
                    trabajo_mayor = porcentajes_yes.idxmax()
                    trabajo_menor = porcentajes_yes.idxmin()
    
                    porcentaje_mayor = porcentajes_yes.max()
                    porcentaje_menor = porcentajes_yes.min()
    
                    diferencia = porcentaje_mayor - porcentaje_menor

                    st.success(f"El trabajo con mayor porcentaje de aceptación es **{trabajo_mayor}**, con **{porcentaje_mayor:.2f} %**.")
                    st.warning(f"El trabajo con menor porcentaje de aceptación es **{trabajo_menor}**, con **{porcentaje_menor:.2f} %**.")
                    st.write(f"La diferencia entre ambos grupos es de **{diferencia:.2f} puntos porcentuales**.")
    
                else:
                    st.warning("No se encontró la categoría `yes` en la variable `y`.")
                    st.write("Categorías encontradas:", tabla_porcentajes.columns.tolist())

            elif variable_2 == "education":
                st.write("Nivel educativo más frecuente dentro de cada tipo de trabajo:")
                interpretaciones = []
                                
                for trabajo in tabla_porcentajes.index:
                    educacion_principal = (tabla_porcentajes.loc[trabajo].idxmax())
                    porcentaje_principal = tabla_porcentajes.loc[trabajo, educacion_principal]
                    cantidad_principal = tabla_frecuencias.loc[trabajo, educacion_principal]

                    interpretaciones.append({
                        "Trabajo": trabajo,
                        "Educación más frecuente": educacion_principal,
                        "Cantidad": int(cantidad_principal),
                        "Porcentaje": f"{porcentaje_principal:.2f} %"
                    })
    
                tabla_interpretacion = pd.DataFrame(interpretaciones)
                st.dataframe(tabla_interpretacion, hide_index=True, use_container_width=True)

                # Interpretación general
                combinacion_mayor = tabla_porcentajes.stack().idxmax()
                porcentaje_combinacion = tabla_porcentajes.stack().max()
        
                trabajo_destacado, educacion_destacada = combinacion_mayor
        
                st.success(f"La concentración porcentual más alta se encuentra en el trabajo **{trabajo_destacado}**, donde el nivel "
                    f"educativo predominante es **{educacion_destacada}**, con **{porcentaje_combinacion:.2f} %**.")

# -----------------------------------------------------------------------------
# Item 9 - Análisis basado en parámetros seleccionados
# ----------------------------------------------------------------------------- 
        with tabs[8]:
            st.markdown('<h2 style="text-align:center;">Análisis basado en parámetros seleccionados</h2>', unsafe_allow_html=True)   
            st.subheader("Selección de columnas")

            var_numericas = obtener_var_numericas(df)
            var_categoricas = obtener_var_categoricas(df)
            st.subheader("Filtros")

            # Copia del DataFrame sobre la cual se aplicarán los filtros
            df_filtrado = df.copy()
  
            # ==========================================================
            # 1. SELECCIONAR VARIABLES CATEGÓRICAS PARA FILTRAR
            # ==========================================================
            columnas_categoricas_filtro = st.multiselect("Seleccione variables categóricas para filtrar", options=var_categoricas)

            for columna in columnas_categoricas_filtro:
            
                # Los valores nulos se muestran como una opción
                serie = (df_filtrado[columna].astype("string").fillna("Sin dato"))
            
                opciones = sorted(serie.unique().tolist())
            
                valores_seleccionados = st.multiselect(f"Seleccione valores de {columna}", options=opciones, default=opciones, key=f"filtro_cat_{columna}")
            
                # Aplicar filtro categórico
                if valores_seleccionados:
                    df_filtrado = df_filtrado[serie.isin(valores_seleccionados)]
                else:
                    df_filtrado = df_filtrado.iloc[0:0]

            # ==========================================================
            # 2. SELECCIONAR VARIABLES NUMÉRICAS PARA FILTRAR
            # ==========================================================
            columnas_numericas_filtro = st.multiselect("Seleccione variables numéricas para filtrar", options=var_numericas)
            
            for columna in columnas_numericas_filtro:
            
                serie = pd.to_numeric(df_filtrado[columna], errors="coerce")
            
                if serie.dropna().empty:
                    st.warning(f"La variable {columna} no contiene valores válidos.")
                    continue
            
                minimo = float(serie.min())
                maximo = float(serie.max())
            
                if minimo == maximo:
                    st.info(f"{columna} contiene un único valor: {minimo:g}")
                    continue
            
                rango_seleccionado = st.slider(
                    f"Seleccione el rango de {columna}",
                    min_value=minimo,
                    max_value=maximo,
                    value=(minimo, maximo),
                    key=f"filtro_num_{columna}"
                )
            
                # Aplicar filtro numérico
                df_filtrado = df_filtrado[serie.between(rango_seleccionado[0], rango_seleccionado[1], inclusive="both")]

                # ==========================================================
                # 3. MOSTRAR RESULTADO
                # ==========================================================
                #st.write(f"Registros originales: **{len(df)}** | Registros filtrados: **{len(df_filtrado)}**")
                
                #st.dataframe(df_filtrado, use_container_width=True)


                # ==========================================================
                # 3. VALIDACIÓN Y RESUMEN DEL FILTRADO
                # ==========================================================
                
                st.markdown('<h2 style="text-align:center;">Análisis basado en parámetros seleccionados</h2>', unsafe_allow_html=True)
                
                total_original = len(df)
                total_filtrado = len(df_filtrado)
                total_eliminado = total_original - total_filtrado
                
                porcentaje_conservado = (total_filtrado / total_original * 100 if total_original > 0 else 0)
                
                col1, col2, col3, col4 = st.columns(4)
                
                col1.metric("Registros originales", total_original)
                col2.metric("Registros filtrados", total_filtrado)
                col3.metric("Registros eliminados", total_eliminado)
                col4.metric("Datos conservados", f"{porcentaje_conservado:.1f}%")
                
                
                if df_filtrado.empty:
                    st.warning("No existen registros para analizar con los filtros aplicados.")
                    st.stop()
                
                # ==========================================================
                # 4. DETERMINAR LAS VARIABLES QUE SE ANALIZARÁN
                # ==========================================================
                
                # Se analizan las columnas que el usuario seleccionó como filtros.
                numericas_analisis = [
                    columna
                    for columna in columnas_numericas_filtro
                    if columna in df_filtrado.columns
                ]
                
                categoricas_analisis = [
                    columna
                    for columna in columnas_categoricas_filtro
                    if columna in df_filtrado.columns
                ]
                
                
                # Si no se seleccionaron filtros, se pueden usar todas las variables.
                if not numericas_analisis and not categoricas_analisis:
                    st.info(
                        "No se seleccionaron columnas para filtrar. "
                        "Se mostrarán gráficos generales del conjunto de datos."
                    )
                
                    # Se limita la cantidad para no saturar la aplicación.
                    numericas_analisis = var_numericas[:4]
                    categoricas_analisis = var_categoricas[:4]

                # ==========================================================
                # 5. GRÁFICOS DE VARIABLES NUMÉRICAS
                # ==========================================================
                
                if numericas_analisis:
                
                    st.subheader("Distribución de variables numéricas")
                
                    for variable in numericas_analisis:
                
                        datos = pd.to_numeric(df_filtrado[variable], errors="coerce").dropna()
                
                        if datos.empty:
                            st.warning(f"La variable {variable} no contiene valores válidos.")
                            continue
                
                        st.markdown(f"#### {variable}")
                        columna_histograma, columna_boxplot = st.columns([2, 1])
                
                        # Histograma
                        with columna_histograma:
                
                            fig, ax = plt.subplots(figsize=(7, 4))
                
                            sns.histplot(
                                datos,
                                bins="auto",
                                kde=True,
                                color="steelblue",
                                ax=ax
                            )
                
                            ax.axvline(
                                datos.mean(),
                                color="red",
                                linestyle="--",
                                label=f"Media: {datos.mean():.2f}"
                            )
                
                            ax.axvline(
                                datos.median(),
                                color="green",
                                linestyle=":",
                                label=f"Mediana: {datos.median():.2f}"
                            )
                
                            ax.set_title(f"Distribución de {variable}")
                            ax.set_xlabel(variable)
                            ax.set_ylabel("Frecuencia")
                            ax.legend()
                
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close(fig)
                
                        # Boxplot
                        with columna_boxplot:
                
                            fig, ax = plt.subplots(figsize=(5, 4))
                
                            sns.boxplot(
                                y=datos,
                                color="orange",
                                ax=ax
                            )
                
                            ax.set_title(f"Boxplot de {variable}")
                            ax.set_ylabel(variable)
                            ax.set_xlabel("")
                
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close(fig)
                
                        # Estadísticas descriptivas
                        with st.expander(f"Ver estadísticas de {variable}"):
                
                            resumen = datos.describe().to_frame("Resultado")
                            resumen.loc["mediana"] = datos.median()
                            resumen.loc["varianza"] = datos.var()
                
                            st.dataframe(
                                resumen,
                                use_container_width=True
                            )
                
                # ==========================================================
                # 7. MATRIZ DE CORRELACIÓN
                # ==========================================================
                
                if len(numericas_analisis) >= 2:
                
                    st.subheader("Relación entre variables numéricas")
                
                    datos_correlacion = (
                        df_filtrado[numericas_analisis]
                        .apply(pd.to_numeric, errors="coerce")
                    )
                
                    # Eliminar variables constantes, porque su correlación es indefinida.
                    columnas_validas = [
                        columna
                        for columna in datos_correlacion.columns
                        if datos_correlacion[columna].nunique(dropna=True) > 1
                    ]
                
                    if len(columnas_validas) >= 2:
                
                        matriz_correlacion = (
                            datos_correlacion[columnas_validas]
                            .corr()
                        )
                
                        fig, ax = plt.subplots(
                            figsize=(
                                max(7, len(columnas_validas)),
                                max(5, len(columnas_validas) * 0.7)
                            )
                        )
                
                        sns.heatmap(
                            matriz_correlacion,
                            annot=True,
                            fmt=".2f",
                            cmap="coolwarm",
                            center=0,
                            vmin=-1,
                            vmax=1,
                            linewidths=0.5,
                            ax=ax
                        )
                
                        ax.set_title("Matriz de correlación")
                
                        plt.tight_layout()
                        st.pyplot(fig)
                        plt.close(fig)
                
                    else:
                        st.info(
                            "No hay suficientes variables numéricas con variación "
                            "para calcular la correlación."
                        )
                
                
                # ==========================================================
                # 8. VARIABLE CATEGÓRICA VS. VARIABLE NUMÉRICA
                # ==========================================================
                
                if categoricas_analisis and numericas_analisis:
                
                    st.subheader("Comparación entre variables categóricas y numéricas")
                
                    # Se generan todas las combinaciones disponibles.
                    combinaciones_mixtas = list(
                        itertools.product(
                            categoricas_analisis,
                            numericas_analisis
                        )
                    )
                
                    # Evita generar demasiados gráficos.
                    maximo_graficos_mixtos = 6
                
                    if len(combinaciones_mixtas) > maximo_graficos_mixtos:
                        st.info(
                            f"Existen {len(combinaciones_mixtas)} combinaciones. "
                            f"Se mostrarán las primeras {maximo_graficos_mixtos}."
                        )
                
                    for variable_cat, variable_num in (
                        combinaciones_mixtas[:maximo_graficos_mixtos]
                    ):
                
                        datos_grafico = df_filtrado[
                            [variable_cat, variable_num]
                        ].copy()
                
                        datos_grafico[variable_cat] = (
                            datos_grafico[variable_cat]
                            .astype("string")
                            .fillna("Sin dato")
                        )
                
                        datos_grafico[variable_num] = pd.to_numeric(
                            datos_grafico[variable_num],
                            errors="coerce"
                        )
                
                        datos_grafico = datos_grafico.dropna(
                            subset=[variable_num]
                        )
                
                        if datos_grafico.empty:
                            continue
                
                        # Ordenar las categorías según la mediana.
                        orden_categorias = (
                            datos_grafico
                            .groupby(variable_cat)[variable_num]
                            .median()
                            .sort_values()
                            .index
                        )
                
                        figura_alto = max(
                            4,
                            min(
                                10,
                                datos_grafico[variable_cat].nunique() * 0.4
                            )
                        )
                
                        fig, ax = plt.subplots(figsize=(9, figura_alto))
                
                        sns.boxplot(
                            data=datos_grafico,
                            x=variable_num,
                            y=variable_cat,
                            order=orden_categorias,
                            color="skyblue",
                            ax=ax
                        )
                
                        ax.set_title(
                            f"Distribución de {variable_num} por {variable_cat}"
                        )
                
                        ax.set_xlabel(variable_num)
                        ax.set_ylabel(variable_cat)
                
                        plt.tight_layout()
                        st.pyplot(fig)
                        plt.close(fig)
                
       
        

# -----------------------------------------------------------------------------
# Item 10 - Hallazgos clave
# ----------------------------------------------------------------------------- 
        with tabs[9]:
            st.markdown('<h2 style="text-align:center;">Hallazgos clave</h2>', unsafe_allow_html=True)   
            
            
            
            
                            
            
                            
            
            


            





