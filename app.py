import streamlit as st
import pandas as pd
import numpy as np

# Configuración de página
st.set_page_config(page_title="DataClean Pro", layout="centered")

# Estilos CSS - Diseño Oscuro Esmeralda/Cian
st.markdown("""
    <style>
        .stApp { background-color: #121824 !important; color: #E5E7EB; }
        h1, h2, h3 { color: #10B981 !important; }
        
        .section-card { 
            background-color: #1E293B; 
            padding: 2rem; 
            border-radius: 16px; 
            border: 1px solid #334155; 
            margin-bottom: 2rem; 
            transition: all 0.3s ease;
        }
        
        /* Botones estilo Esmeralda */
        div.stButton > button {
            background-color: transparent !important;
            border: 2px solid #10B981 !important;
            color: #10B981 !important;
            border-radius: 8px !important;
            width: 100%;
            font-weight: bold;
        }
        div.stButton > button:hover {
            background-color: #10B981 !important;
            color: #121824 !important;
        }
        
        /* Inputs y File Uploader */
        .stFileUploader { border: 2px dashed #06B6D4 !important; border-radius: 12px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧼 DataClean Pro")
st.markdown("### Flujo de Trabajo Continuo")

# --- Sección 1: Carga ---
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("1. Ingesta de Datos")
    uploaded_file = st.file_uploader("Sube tu archivo (CSV/XLSX)", type=["csv", "xlsx"])
    st.markdown('</div>', unsafe_allow_html=True)

# --- Lógica de procesamiento ---
if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # Limpieza de nulos textuales
    def limpiar_nulos_textuales(df):
        nulos_textuales = ['none', 'nan', 'null', 'n/a', 'na', 'nat', 'nil', '']
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(lambda x: np.nan if str(x).strip().lower() in nulos_textuales else x)
        return df

    df = limpiar_nulos_textuales(df)

    # --- Sección 2: Acción ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("2. Ejecución de Limpieza")
    if st.button("🚀 Iniciar Proceso de Purificación"):
        df_cleaned = df.copy()
        for col in df_cleaned.columns:
            if df_cleaned[col].isnull().any():
                if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                    df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
                else:
                    moda = df_cleaned[col].mode()
                    fill_val = moda[0] if not moda.empty else "No Especificado"
                    df_cleaned[col] = df_cleaned[col].fillna(fill_val)
        
        for col in df_cleaned.select_dtypes(include='object').columns:
            df_cleaned[col] = df_cleaned[col].apply(lambda x: str(x).strip().title() if pd.notnull(x) else x)
        
        st.session_state['df_cleaned'] = df_cleaned
        st.success("✅ ¡Datos purificados! Se ha desbloqueado la descarga.")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Sección 3: Resultados ---
    if 'df_cleaned' in st.session_state:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("3. Resultados y Descarga")
        st.dataframe(st.session_state['df_cleaned'], use_container_width=True)
        
        csv = st.session_state['df_cleaned'].to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Archivo Optimizado", csv, "archivo_limpio.csv", "text/csv")
        st.markdown('</div>', unsafe_allow_html=True)