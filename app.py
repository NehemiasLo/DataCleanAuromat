import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os

# ---------------------------------------------------------
# Configuración de la página web
# ---------------------------------------------------------
st.set_page_config(
    page_title="DataClean - Limpieza Inteligente de Datos",
    page_icon="🧼",
    layout="wide"
)

# ---------------------------------------------------------
# Estilos CSS Personalizados: Diseño Minimalista Premium e Industrial
# ---------------------------------------------------------
st.markdown("""
    <style>
        /* Importar tipografía limpia */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Aplicar tipografía general */
        html, body, [class*="css"], .stMarkdown {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        /* Fondo general ultra claro y limpio */
        .stApp {
            background-color: #F8F9FA !important;
        }

        /* Cabecera minimalista */
        .main-header {
            text-align: center;
            padding: 2.5rem 0 1rem 0;
            background-color: #F8F9FA;
        }
        .main-header h1 {
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            color: #111827 !important;
            letter-spacing: -0.05em !important;
            margin-bottom: 0.5rem !important;
        }
        .main-header p {
            font-size: 1.1rem !important;
            color: #6B7280 !important;
            font-weight: 300 !important;
        }

        /* Guía de Pasos Horizontal */
        .step-container {
            display: flex;
            justify-content: space-around;
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0 2rem 0;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        }
        .step-item {
            text-align: center;
            flex: 1;
        }
        .step-number {
            display: inline-block;
            width: 28px;
            height: 28px;
            line-height: 28px;
            border-radius: 50%;
            background-color: #1E3A8A;
            color: #FFFFFF;
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 0.25rem;
        }
        .step-text {
            font-size: 0.85rem;
            color: #374151;
            font-weight: 500;
            display: block;
        }

        /* Tarjetas blancas con bordes redondeados y sombras sutiles */
        div.stBox, div[data-testid="stMetric"], .element-container iframe, div[data-testid="stForm"] {
            border: 1px solid #E5E7EB !important;
            background-color: #FFFFFF !important;
            border-radius: 12px !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03) !important;
            padding: 1.25rem !important;
        }

        /* Estilo para las métricas dentro de las tarjetas */
        div[data-testid="stMetric"] {
            border: 1px solid #F3F4F6 !important;
            padding: 1.25rem !important;
            background: #FFFFFF !important;
        }

        /* Contenedores y espaciados de bloque para simular tarjetas */
        .custom-card {
            background-color: #FFFFFF;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.025);
        }

        /* Zona de arrastrar archivos estilizada (File Uploader) */
        section[data-testid="stFileUploader"] {
            border: 2px dashed #D1D5DB !important;
            background-color: #FFFFFF !important;
            border-radius: 12px !important;
            padding: 2.5rem 2rem !important;
            transition: border-color 0.2s ease;
        }
        section[data-testid="stFileUploader"]:hover {
            border-color: #1E3A8A !important;
        }

        /* Ocultar etiquetas e instrucciones innecesarias en el cargador para mayor limpieza */
        section[data-testid="stFileUploader"] label {
            font-weight: 500 !important;
            font-size: 1.05rem !important;
            color: #374151 !important;
            margin-bottom: 0.75rem !important;
        }

        /* Botones principales: Azul Marino Elegante */
        div.stButton > button[kind="primary"] {
            background-color: #1E3A8A !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 500 !important;
            padding: 0.65rem 1.75rem !important;
            border-radius: 8px !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
            transition: all 0.2s ease-in-out !important;
            width: 100% !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #172E6F !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        }

        /* Botones secundarios / Botón de descarga */
        div.stButton > button[kind="secondary"], .stDownloadButton > button {
            background-color: #FFFFFF !important;
            color: #1E3A8A !important;
            border: 1px solid #1E3A8A !important;
            font-weight: 500 !important;
            padding: 0.65rem 1.75rem !important;
            border-radius: 8px !important;
            transition: all 0.2s ease-in-out !important;
            width: 100% !important;
        }
        div.stButton > button[kind="secondary"]:hover, .stDownloadButton > button:hover {
            background-color: #F1F5F9 !important;
            border-color: #172E6F !important;
            color: #172E6F !important;
        }

        /* Sutil ajuste para las líneas de separación */
        hr {
            margin: 2.5rem 0 !important;
            border: 0 !important;
            border-top: 1px solid #E5E7EB !important;
        }

        /* Encabezados secundarios limpios e industriales */
        h2, h3, h4 {
            color: #111827 !important;
            font-weight: 600 !important;
            letter-spacing: -0.03em !important;
        }

        /* Ajustar alertas para que se vean minimalistas */
        .stAlert {
            border-radius: 8px !important;
            border: 1px solid #E5E7EB !important;
            background-color: #FAFAFA !important;
        }
    </style>
""", unsafe_allowed_html=True)

# ---------------------------------------------------------
# Encabezado Minimalista Premium
# ---------------------------------------------------------
st.markdown("""
    <div class="main-header">
        <h1>DataClean</h1>
        <p>Sube, limpia y descarga tu base de datos optimizada en segundos, sin complicaciones técnicas.</p>
    </div>
""", unsafe_allowed_html=True)

# Guía Visual de Pasos para el usuario final
st.markdown("""
    <div class="step-container">
        <div class="step-item">
            <span class="step-number">1</span>
            <span class="step-text">Subir Datos (o usar Prueba)</span>
        </div>
        <div class="step-item">
            <span class="step-number">2</span>
            <span class="step-text">Revisar Diagnóstico</span>
        </div>
        <div class="step-item">
            <span class="step-number">3</span>
            <span class="step-text">Ejecutar Limpieza</span>
        </div>
        <div class="step-item">
            <span class="step-number">4</span>
            <span class="step-text">Descargar Archivo Pulido</span>
        </div>
    </div>
""", unsafe_allowed_html=True)


# ---------------------------------------------------------
# Generador de Dataset de Prueba Sucio (Para Testing Rápido)
# ---------------------------------------------------------
def load_sample_dataset():
    data = {
        'ID_Cliente': [101, 102, 103, 104, 104, 105, 106, 107],
        'Nombre_Completo': ['  juan perez  ', 'Marta Gómez', 'Carlos Ruiz', 'ana logan', 'ana logan', 'luis Fernandez',
                            'Sofía herrera', 'Pedro Almodovar'],
        'Ciudad': ['medellin', 'Medellín', 'MEDELLIN', 'bogota', 'bogota', 'Cali', '  medellín ', 'Bogotá D.C.'],
        'Ventas': ['$1.500,00', '€ 2.300', '1800', '$-500', '$-500', np.nan, '€3500', '12500'],
        'Edad': [34, 150, 42, 29, 29, 31, np.nan, 45],
        'Fecha_Registro': ['2026/01/15', '16-01-2026', '2026.01.17', '2026/01/18', '2026/01/18', '2026-01-19', np.nan,
                           '2026-01-21']
    }
    return pd.DataFrame(data)


# ---------------------------------------------------------
# 1. Carga de Archivos
# ---------------------------------------------------------
st.markdown('<div class="custom-card">', unsafe_allowed_html=True)
st.subheader("Paso 1: Sube tu base de datos")
uploaded_file = st.file_uploader(
    "Selecciona o arrastra tu archivo aquí (Admite planillas de Excel .xlsx y archivos de datos .csv)",
    type=["csv", "xlsx"]
)

# Botón interactivo para usar datos de prueba si no se tiene un archivo listo
st.markdown(
    "<p style='text-align: center; color: #6B7280; font-size: 0.9rem; margin: 1rem 0 0.5rem 0;'>¿No tienes un archivo a la mano para probar?</p>",
    unsafe_allowed_html=True)
col_btn_test, _ = st.columns([1, 2])
with col_btn_test:
    use_sample = st.button("🧪 Cargar datos de prueba desordenados", type="secondary")

st.markdown('</div>', unsafe_allowed_html=True)

# Determinar origen de datos (archivo subido o simulación de prueba)
df = None
file_name_display = ""

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        file_name_display = uploaded_file.name
        st.session_state['using_sample'] = False
    except Exception as e:
        st.error(f"Error al leer el archivo cargado: {e}")

elif use_sample or st.session_state.get('using_sample', False):
    df = load_sample_dataset()
    file_name_display = "dataset_prueba_desordenado.csv"
    st.session_state['using_sample'] = True
    st.info(
        "Se ha cargado el dataset de prueba con errores comunes (duplicados, nulos, problemas de escritura, formatos monetarios inconsistentes y valores extremos).")

# ---------------------------------------------------------
# Si hay datos listos para procesar
# ---------------------------------------------------------
if df is not None:
    try:
        # ---------------------------------------------------------
        # 2. Diagnóstico Inicial del Dataset
        # ---------------------------------------------------------
        st.markdown('<div class="custom-card">', unsafe_allowed_html=True)
        st.subheader("Paso 2: Diagnóstico de Calidad de Datos")
        st.markdown(
            "<p style='color:#6B7280; font-size:0.9rem; margin-bottom:1.5rem;'>El sistema ha analizado tu archivo y encontró los siguientes detalles estructurales:</p>",
            unsafe_allowed_html=True)

        col1, col2 = st.columns([2, 1], gap="large")

        with col1:
            st.markdown("**Vista previa de tus datos originales:**")
            st.dataframe(df, use_container_width=True)

        with col2:
            st.markdown("**Resumen de inconsistencias encontradas:**")
            total_filas, total_cols = df.shape
            filas_duplicadas = int(df.duplicated().sum())
            total_nulos = int(df.isnull().sum().sum())

            st.metric(label="Total de Celdas de Datos", value=f"{total_filas} filas x {total_cols} col.")
            st.metric(label="Filas Repetidas (Duplicadas)", value=filas_duplicadas,
                      delta=-filas_duplicadas if filas_duplicadas > 0 else 0, delta_color="inverse")
            st.metric(label="Celdas Vacías (Nulos)", value=total_nulos, delta=-total_nulos if total_nulos > 0 else 0,
                      delta_color="inverse")
        st.markdown('</div>', unsafe_allowed_html=True)

        # ---------------------------------------------------------
        # 3. Pipeline interactivo de Limpieza Inteligente
        # ---------------------------------------------------------
        st.markdown('<div class="custom-card">', unsafe_allowed_html=True)
        st.subheader("Paso 3: Personalizar y Ejecutar Limpieza")
        st.markdown(
            "<p style='color:#6B7280; font-size:0.95rem; margin-bottom:1.5rem;'>Elige qué operaciones automáticas deseas aplicar al dataset (están todas activadas por defecto para una limpieza óptima):</p>",
            unsafe_allowed_html=True)

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            clean_duplicates = st.checkbox("Eliminar filas repetidas/duplicadas", value=True,
                                           help="Remueve copias idénticas exactas en los registros.")
            clean_text = st.checkbox("Estandarizar textos y nombres", value=True,
                                     help="Quita espacios innecesarios, capitaliza nombres y corrige variaciones ortográficas de ciudades comunes como 'Medellín'.")
            clean_currencies = st.checkbox("Corregir e igualar formatos de monedas", value=True,
                                           help="Detecta símbolos de divisas (€, $, ¥) y estandariza los montos a formato numérico limpio.")
        with col_opt2:
            clean_nulls = st.checkbox("Rellenar celdas vacías de forma inteligente", value=True,
                                      help="Completa textos faltantes con el valor más frecuente y números vacíos utilizando el promedio estadístico (mediana).")
            clean_outliers = st.checkbox("Moderar valores extremos y corregir negativos", value=True,
                                         help="Identifica números fuera de lo común causados por errores tipográficos (ej. edad de 150) y los ajusta a valores lógicos.")
            infer_types = st.checkbox("Autodetectar y convertir fechas/números", value=True,
                                      help="Corrige formatos de columnas que deberían ser fechas o números pero se guardaron como texto.")

        st.markdown("<br>", unsafe_allowed_html=True)

        if st.button("✨ Iniciar Limpieza Automática de Datos", type="primary"):
            with st.spinner("Saneando estructura, corrigiendo inconsistencias y puliendo tus datos..."):

                df_cleaned = df.copy()
                logs = []

                # --- A. Eliminar duplicados ---
                if clean_duplicates:
                    dupes_before = df_cleaned.duplicated().sum()
                    if dupes_before > 0:
                        df_cleaned = df_cleaned.drop_duplicates().reset_index(drop=True)
                        logs.append(f"Se eliminaron **{dupes_before} filas repetidas** para asegurar registros únicos.")

                # --- B. Inferencia de Tipos ---
                if infer_types:
                    for col in df_cleaned.columns:
                        if 'date' in col.lower() or 'fecha' in col.lower():
                            temp_series = pd.to_datetime(df_cleaned[col], errors='coerce')
                            if temp_series.notna().sum() / len(df_cleaned) > 0.6 and temp_series.notna().sum() > 0:
                                df_cleaned[col] = temp_series
                                logs.append(f"La columna **'{col}'** se formateó correctamente como Fecha.")
                                continue

                        temp_series = pd.to_numeric(df_cleaned[col], errors='coerce')
                        if not pd.api.types.is_numeric_dtype(df_cleaned[col]) and (
                                temp_series.notna().sum() / len(df_cleaned) > 0.8):
                            df_cleaned[col] = temp_series
                            logs.append(f"La columna de texto **'{col}'** se transformó a tipo Numérico.")
                            continue

                # --- C. Formatos de Moneda ---
                if clean_currencies:
                    for col in df_cleaned.select_dtypes(include='object').columns:
                        combined_string = ' '.join(df_cleaned[col].astype(str).dropna().tolist())
                        currency_pattern = r'[€$£¥]'
                        if pd.Series(combined_string).str.contains(currency_pattern, regex=True).any():

                            cleaned_series = df_cleaned[col].astype(str).str.replace(currency_pattern, '', regex=True)
                            num_commas = cleaned_series.str.count(',').sum()
                            num_dots = cleaned_series.str.count('\.').sum()

                            if num_commas > num_dots and num_commas > 0:
                                cleaned_series = cleaned_series.str.replace('.', '', regex=False).str.replace(',', '.',
                                                                                                              regex=False)
                            else:
                                cleaned_series = cleaned_series.str.replace(',', '', regex=False)

                            df_cleaned[col] = pd.to_numeric(cleaned_series, errors='coerce')
                            logs.append(
                                f"Se corrigieron y unificaron los formatos monetarios en la columna **'{col}'**.")

                # --- D. Tratamiento de Outliers y Negativos ---
                if clean_outliers:
                    for col in df_cleaned.select_dtypes(include=np.number).columns:
                        if df_cleaned[col].dropna().empty:
                            continue

                        # Saneamiento de Negativos en variables de conteo/ventas que deben ser positivas
                        negative_mask = df_cleaned[col] < 0
                        negative_count = negative_mask.sum()
                        if negative_count > 0:
                            median_non_negative = df_cleaned[df_cleaned[col] >= 0][col].median()
                            if pd.isna(median_non_negative):
                                median_non_negative = df_cleaned[col].median()
                            df_cleaned.loc[negative_mask, col] = median_non_negative
                            logs.append(
                                f"En **'{col}'** se corrigieron **{negative_count} valores negativos** incoherentes.")

                        # Tratamiento de Outliers estadísticos (IQR)
                        Q1 = df_cleaned[col].quantile(0.25)
                        Q3 = df_cleaned[col].quantile(0.75)
                        IQR = Q3 - Q1
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR

                        outliers_mask = (df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound)
                        outliers_count = outliers_mask.sum()
                        if outliers_count > 0:
                            median_val = df_cleaned[col].median()
                            df_cleaned.loc[outliers_mask, col] = median_val
                            logs.append(
                                f"En **'{col}'** se normalizaron **{outliers_count} valores extremadamente desproporcionados** (ej. errores de digitación).")

                # --- E. Imputación de Valores Faltantes ---
                if clean_nulls:
                    for col in df_cleaned.columns:
                        if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                            if df_cleaned[col].isnull().any():
                                median_val = df_cleaned[col].median()
                                df_cleaned[col] = df_cleaned[col].fillna(median_val)
                                logs.append(
                                    f"Celdas vacías en la columna numérica **'{col}'** completadas con su mediana ({median_val}).")
                        elif pd.api.types.is_object_dtype(df_cleaned[col]):
                            df_cleaned[col] = df_cleaned[col].replace(
                                {'': np.nan, 'nan': np.nan, 'NaN': np.nan, 'None': np.nan, 'N/A': np.nan})
                            df_cleaned[col] = df_cleaned[col].replace(r'^\s*$', np.nan, regex=True)

                            if df_cleaned[col].isnull().any():
                                mode_val = df_cleaned[col].mode()[0] if not df_cleaned[
                                    col].mode().empty else 'No Especificado'
                                df_cleaned[col] = df_cleaned[col].fillna(mode_val)
                                logs.append(
                                    f"Celdas vacías de texto en **'{col}'** completadas con el término más común: '{mode_val}'.")

                # --- F. Organización de Texto y Ortografía ---
                if clean_text:
                    for col in df_cleaned.select_dtypes(include=['object']).columns:
                        if df_cleaned[col].notna().any():
                            df_cleaned[col] = df_cleaned[col].astype(str)
                            # Limpiar espacios en los extremos y capitalizar de manera limpia
                            df_cleaned[col] = df_cleaned[col].str.strip()

                            # Corrección específica de ciudades comunes como "Medellín"
                            if 'ciudad' in col.lower() or 'municipio' in col.lower() or 'departamento' in col.lower():
                                medellin_variations = ['Medellín', 'Medellin', 'medellín', 'MEDELLIN', 'MEdellin',
                                                       'medellín ']
                                for var in medellin_variations:
                                    df_cleaned[col] = df_cleaned[col].str.replace(var, 'Medellín', case=False,
                                                                                  regex=False)

                                # Estandarización de Bogotá
                                bogota_variations = ['Bogotá', 'Bogota', 'bogota', 'BOGOTA', 'Bogotá D.C.',
                                                     'Bogota D.C.']
                                for var in bogota_variations:
                                    df_cleaned[col] = df_cleaned[col].str.replace(var, 'Bogotá', case=False,
                                                                                  regex=False)

                            df_cleaned[col] = df_cleaned[col].str.title()
                    logs.append(
                        "Se eliminaron espacios fantasmas al inicio/final de los textos y se estandarizaron mayúsculas de nombres.")

                # Guardar en el estado de la sesión
                st.session_state['df_cleaned'] = df_cleaned
                st.session_state['logs'] = logs
                st.success("¡Tu dataset ha sido purificado con éxito!")
        st.markdown('</div>', unsafe_allowed_html=True)

        # ---------------------------------------------------------
        # 4. Presentación de Resultados y Descarga
        # ---------------------------------------------------------
        if 'df_cleaned' in st.session_state:
            df_final = st.session_state['df_cleaned']
            logs_finales = st.session_state['logs']

            # --- TAB COMPARATIVA ANTES VS DESPUÉS ---
            st.markdown('<div class="custom-card">', unsafe_allowed_html=True)
            st.subheader("Paso 4: Comparativa y Descarga de Resultados")

            tab_comparacion, tab_detalles, tab_visualizar = st.tabs(
                ["📊 Comparativa de Datos", "📋 Historial de Correcciones", "📈 Exploración Gráfica"])

            with tab_comparacion:
                col_antes, col_despues = st.columns(2)
                with col_antes:
                    st.markdown("<p style='color: #EF4444; font-weight: 600;'>❌ Dataset Original (Con errores):</p>",
                                unsafe_allowed_html=True)
                    st.dataframe(df.head(10), use_container_width=True)
                    st.caption(f"Filas originales: {df.shape[0]} | Columnas: {df.shape[1]}")
                with col_despues:
                    st.markdown("<p style='color: #10B981; font-weight: 600;'>✅ Dataset Optimizado (Limpio):</p>",
                                unsafe_allowed_html=True)
                    st.dataframe(df_final.head(10), use_container_width=True)
                    st.caption(f"Filas limpias: {df_final.shape[0]} | Columnas: {df_final.shape[1]}")

            with tab_detalles:
                st.markdown(
                    "<p style='color:#374151; font-weight: 500;'>Detalle de acciones tomadas de forma automática:</p>",
                    unsafe_allowed_html=True)
                if logs_finales:
                    for log in logs_finales:
                        st.markdown(
                            f"<div style='color:#4B5563; font-size:0.95rem; margin-bottom:0.5rem; padding-left:0.75rem; border-left:3px solid #1E3A8A;'>{log}</div>",
                            unsafe_allowed_html=True)
                else:
                    st.markdown(
                        "<p style='color:#6B7280;'>No se requirieron modificaciones. El dataset cumple con todos los estándares de producción.</p>",
                        unsafe_allowed_html=True)

            with tab_visualizar:
                numerical_cols = df_final.select_dtypes(include=np.number).columns
                categorical_cols = df_final.select_dtypes(include=['object']).columns
                brand_color = '#1E3A8A'

                if not numerical_cols.empty or not categorical_cols.empty:
                    st.markdown(
                        "<p style='color:#6B7280; font-size:0.9rem; margin-bottom:1.5rem;'>Gráficos generados para entender las variables del archivo limpio:</p>",
                        unsafe_allowed_html=True)

                    if not numerical_cols.empty:
                        for col in numerical_cols:
                            fig, ax = plt.subplots(figsize=(7, 2.2), facecolor='none')
                            sns.histplot(df_final[col], kde=True, ax=ax, color=brand_color, edgecolor='#ffffff',
                                         alpha=0.8)
                            ax.set_facecolor('none')
                            ax.spines['top'].set_visible(False)
                            ax.spines['right'].set_visible(False)
                            ax.spines['left'].set_color('#D1D5DB')
                            ax.spines['bottom'].set_color('#D1D5DB')
                            ax.tick_params(colors='#4B5563', labelsize=8)
                            ax.set_title(f'Distribución de {col}', color='#111827', fontsize=10, pad=8,
                                         weight='semibold')
                            st.pyplot(fig)
                            plt.close(fig)

                    if not categorical_cols.empty:
                        for col in categorical_cols:
                            top_10 = df_final[col].value_counts().nlargest(10)
                            if not top_10.empty:
                                fig, ax = plt.subplots(figsize=(7, 2.8), facecolor='none')
                                sns.barplot(x=top_10.index, y=top_10.values,
                                            palette=sns.color_palette("Blues_r", len(top_10)), ax=ax)
                                ax.set_facecolor('none')
                                ax.spines['top'].set_visible(False)
                                ax.spines['right'].set_visible(False)
                                ax.spines['left'].set_color('#D1D5DB')
                                ax.spines['bottom'].set_color('#D1D5DB')
                                ax.tick_params(colors='#4B5563', labelsize=8)
                                ax.set_title(f'Top 10 Valores de la columna {col}', color='#111827', fontsize=10, pad=8,
                                             weight='semibold')
                                plt.xticks(rotation=45, ha='right')
                                st.pyplot(fig)
                                plt.close(fig)
                else:
                    st.markdown(
                        "<p style='color:#6B7280;'>No hay columnas numéricas ni categóricas suficientes para estructurar visualizaciones.</p>",
                        unsafe_allowed_html=True)

            # --- Descarga directa del archivo pulido ---
            st.markdown("<hr>", unsafe_allowed_html=True)
            st.markdown(
                "<p style='text-align: center; color:#374151; font-weight: 500;'>¿Todo listo? Descarga tu archivo purificado aquí:</p>",
                unsafe_allowed_html=True)


            @st.cache_data
            def convert_df(df_to_convert):
                return df_to_convert.to_csv(index=False).encode('utf-8')


            csv_bytes = convert_df(df_final)
            base_name = os.path.splitext(file_name_display)[0]

            st.download_button(
                label="📥 Descargar Base de Datos Limpia (Formato CSV)",
                data=csv_bytes,
                file_name=f"{base_name}_limpio.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allowed_html=True)

    except Exception as e:
        st.markdown(f"""
            <div style='padding:1.5rem; background-color:#FEF2F2; border:1px solid #FCA5A5; border-radius:8px; color:#991B1B; margin-top:2rem;'>
                <strong>Ocurrió un inconveniente al procesar la planilla:</strong> {e}
            </div>
        """, unsafe_allowed_html=True)
