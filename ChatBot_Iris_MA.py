# pip install streamlit

import streamlit as st
import pandas as pd
from langchain.llms import OpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# 📌 Sidebar para ingresar la clave
st.sidebar.title("🔑 Configuración")
api_key = st.sidebar.text_input("Ingresa tu OpenAI API Key:", type="password")

# ✅ Título
st.title("📊 Chatbot de Tabla de Datos")

# 📁 Subida del archivo
uploaded_file = st.file_uploader("Carga tu archivo CSV", type="csv")

if api_key:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Vista previa de los datos:")
        st.dataframe(df)

        # 🧠 Crear modelo con la clave ingresada
        llm = OpenAI(temperature=0, openai_api_key=api_key)
        agent = create_pandas_dataframe_agent(llm, df, verbose=False, allow_dangerous_code=True)

        # Chatbox de pregunta
        question = st.text_input("Haz una pregunta sobre la tabla:")

        if question:
            with st.spinner("Pensando..."):
                try:
                    response = agent.run(question)
                    st.success(response)
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.warning("Por favor, ingresa tu OpenAI API Key en la barra lateral para continuar.")
    
# ls -> enlista documentos
# cd -> cambia de directorio

# streamlit run pruebaSt.py
