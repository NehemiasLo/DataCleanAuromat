import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración de página
st.set_page_config(page_title="DataClean Pro", layout="wide")

# Estilos CSS
st.markdown("""
    <style>
        .custom-card { background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("🧼 DataClean Inteligente")

# Carga de archivos
uploaded_file = st.file_uploader("Sube tu archivo (CSV/XLSX)", type=["csv", "xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    # --- LA CORRECCIÓN CRÍTICA ESTÁ AQUÍ ---
    # Convertimos cualquier representación textual de nulos a NaN real antes de procesar nada
    def limpiar_nulos_textuales(df):
        nulos_textuales = ['none', 'nan', 'null', 'n/a', 'na', 'nat', 'nil', '']
        for col in df.columns:
            if df[col].dtype == 'object':
                # Convertimos todo a string, limpiamos espacios y comparamos
                df[col] = df[col].apply(lambda x: np.nan if str(x).strip().lower() in nulos_textuales else x)
        return df

    df = limpiar_nulos_textuales(df)
    
    if st.button("🚀 Limpiar Dataset"):
        df_cleaned = df.copy()
        
        # 1. Imputación inteligente de nulos (ahora que son NaNs reales)
        for col in df_cleaned.columns:
            if df_cleaned[col].isnull().any():
                if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                    df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
                else:
                    # Rellenar con la moda de los datos válidos
                    moda = df_cleaned[col].mode()
                    fill_val = moda[0] if not moda.empty else "No Especificado"
                    df_cleaned[col] = df_cleaned[col].fillna(fill_val)
        
        # 2. Limpieza de texto (sin reintroducir "None")
        for col in df_cleaned.select_dtypes(include='object').columns:
            df_cleaned[col] = df_cleaned[col].apply(lambda x: str(x).strip().title() if pd.notnull(x) else x)

        st.session_state['df_cleaned'] = df_cleaned
        st.success("¡Datos purificados!")

    if 'df_cleaned' in st.session_state:
        df_final = st.session_state['df_cleaned']
        st.subheader("Resultado Limpio")
        st.dataframe(df_final)
        
        # Descarga
        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Limpio", csv, "archivo_limpio.csv", "text/csv")