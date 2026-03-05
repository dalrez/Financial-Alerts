import pandas as pd
import streamlit as st

st.set_page_config(page_title="IBEX35 - Bajo SMA200", layout="wide")
st.title("IBEX35 – Empresas bajo SMA200")

path = "data/under_sma200.csv"

try:
    df = pd.read_csv(path)
except FileNotFoundError:
    st.warning("Aún no existe data/under_sma200.csv. Ejecuta el workflow una vez.")
    st.stop()

if df.empty:
    st.info("No hay empresas bajo SMA200 (según la lista actual).")
else:
    st.subheader("Listado")
    st.dataframe(df, use_container_width=True)

    st.subheader("Resumen")
    st.write(f"Total: {len(df)} empresas")
    st.write("Más por debajo de la SMA200 (más negativo):")
    st.dataframe(df.sort_values("PctBelow").head(10), use_container_width=True)
