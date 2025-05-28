# pip install streamlit

import streamlit as st
import pandas as pd
import os
from langchain.llms import OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# Sidebar para ingresar la clave
st.sidebar.title("🔑 Configuración")
api_key = st.sidebar.text_input("Ingresa tu OpenAI API Key:", type="password")

# Título principal
st.title("📊 Chatbot de Tabla de Datos")

# Subida del archivo
uploaded_file = st.file_uploader("Carga tu archivo CSV", type="csv")

# Función para validar si la pregunta es relevante para la tabla
def pregunta_relevante(pregunta, df):
    columnas = [col.lower() for col in df.columns]
    palabras_clave = ["promedio", "valor", "columna", "dato", "medida", "máximo", "mínimo", "frecuencia", "total", "cantidad", "producto"]
    palabras_validas = columnas + palabras_clave
    return any(palabra in pregunta.lower() for palabra in palabras_validas)

# Solo continúa si hay clave ingresada
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key  # Establece variable de entorno

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Vista previa de los datos:")
        st.dataframe(df)

        llm = OpenAI(temperature=0)
        agent = create_pandas_dataframe_agent(llm, df, verbose=False, allow_dangerous_code=True)

        # Chatbox
        question = st.text_input("Haz una pregunta sobre la tabla:")

        if question:
            if pregunta_relevante(question, df):
                with st.spinner("Pensando..."):
                    try:
                        response = agent.run(question)
                        st.success(response)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Tu pregunta no está relacionada con los datos disponibles en la tabla.")
else:
    st.warning("Por favor, ingresa tu OpenAI API Key en la barra lateral para continuar.")
    
# ls -> enlista documentos
# cd -> cambia de directorio

# streamlit run pruebaSt.py
