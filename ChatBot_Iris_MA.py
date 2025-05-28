# pip install streamlit

import streamlit as st
import pandas as pd
from langchain.llms import OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import os

# 📌 Sidebar para ingresar la clave
st.sidebar.title("🔑 Configuración")
api_key = st.sidebar.text_input("Ingresa tu OpenAI API Key:", type="password")

# Título
st.title("📊 Chatbot de Tabla de Datos: ")

# Subida del archivo
uploaded_file = st.file_uploader("C:/Users/aguia/OneDrive/MAESTRIA/FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL/EJERCICIO5/iris.csv", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Vista previa de los datos:")
    st.dataframe(df)

    # Crear agente
    llm = OpenAI(temperature=0)
    agent = create_pandas_dataframe_agent(llm, df, verbose=False, allow_dangerous_code=True)

    # 🔽 Aquí colocas la validación una vez df está definido
    columnas = [col.lower() for col in df.columns]
    palabras_clave = ["pétalo", "longitud", "ancho", "medida", "especie", "cantidad"]
    palabras_validas = columnas + palabras_clave

    # Input de usuario
    question = st.text_input("Haz una pregunta sobre la tabla:", key="pregunta_usuario")

    if question:
        if any(palabra in question.lower() for palabra in palabras_validas):
            with st.spinner("Pensando..."):
                try:
                    response = agent.run(question)
                    st.success(response)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Tu pregunta no está relacionada con los datos disponibles en la tabla.")
# ls -> enlista documentos
# cd -> cambia de directorio

# streamlit run pruebaSt.py