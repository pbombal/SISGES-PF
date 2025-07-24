
import streamlit as st
import pandas as pd
from pathlib import Path
import io

st.set_page_config(page_title="Reportería Planes Formativos", layout="wide")

st.title("📊 Reportería de Planes Formativos")
st.markdown("Visualiza, filtra y exporta la base de módulos extraídos desde los Planes Formativos del catálogo SENCE.")

# Ruta del archivo Excel
archivo = Path(__file__).resolve().parent.parent / "data" / "modulos.xlsx"

if not archivo.exists():
    st.error("❌ El archivo modulos.xlsx no fue encontrado en la carpeta /data. Ejecuta el script de consolidación primero.")
    st.stop()

# Cargar datos
df = pd.read_excel(archivo, engine="openpyxl")

# Filtros
with st.sidebar:
    st.header("🔍 Filtros")
    areas = df["Área"].dropna().unique()
    codigos = df["Código PF"].dropna().unique()

    area_sel = st.multiselect("Filtrar por Área", sorted(areas))
    codigo_sel = st.multiselect("Filtrar por Código PF", sorted(codigos))

# Aplicar filtros
df_filtrado = df.copy()

if area_sel:
    df_filtrado = df_filtrado[df_filtrado["Área"].isin(area_sel)]

if codigo_sel:
    df_filtrado = df_filtrado[df_filtrado["Código PF"].isin(codigo_sel)]

st.success(f"✅ {len(df_filtrado)} registros encontrados")

# Mostrar tabla
st.dataframe(df_filtrado, use_container_width=True)

# Crear buffer de Excel para descarga
output = io.BytesIO()
df_filtrado.to_excel(output, index=False, engine="openpyxl")
output.seek(0)

# Botón de descarga
st.download_button(
    label="📥 Descargar Excel filtrado",
    data=output,
    file_name="modulos_filtrados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
