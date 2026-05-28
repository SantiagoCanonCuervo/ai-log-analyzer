import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# 1. Configuración de entorno
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Error: No se encontró la API KEY en tu archivo .env.")
    st.stop()

# Inicializar cliente de Google GenAI
client = genai.Client(api_key=api_key)

# 2. Interfaz
st.set_page_config(page_title="Analizador Senior de Logs", page_icon="🚀")
st.title("🚀 Analizador de Logs - Nivel Senior")
st.write("Sube tus archivos de log o pega el error de consola directamente.")

# Entradas
uploaded_files = st.file_uploader("Subir archivos (.log/.txt):", type=['log', 'txt'], accept_multiple_files=True)
error_text = st.text_area("O pega el error de consola aquí:", placeholder="Pega el traceback o logs manualmente...")

# 3. Lógica de Análisis
if st.button("Analizar con potencia máxima"):
    datos_analisis = ""
    
    # Recopilar archivos
    if uploaded_files:
        for f in uploaded_files:
            datos_analisis += f"\n--- ARCHIVO: {f.name} ---\n{f.read().decode('utf-8')}\n"
    
    # Recopilar texto manual
    if error_text.strip():
        datos_analisis += f"\n--- ERROR DE CONSOLA ---\n{error_text}\n"

    if not datos_analisis.strip():
        st.warning("Por favor, proporciona al menos un archivo o pega algún error.")
    # ... después de las validaciones if not datos_analisis ...
    else:
        # ELIMINAMOS EL ST.SPINNER AQUÍ, YA QUE EL STREAMING ES TU INDICADOR DE CARGA
        try:
            # Instrucción técnica
            prompt = f"""
            Actúa como un ingeniero senior de DevOps. Tu tarea es realizar un diagnóstico técnico.
            
            Instrucciones estrictas:
            1. Identifica errores y advertencias críticas.
            2. Crea una TABLA con: [Origen], [Línea], [Tipo de Error], [Descripción].
            3. Proporciona una explicación técnica detallada del fallo.
            4. Ofrece soluciones concretas (comandos o cambios de código).
            
            LOGS/DATOS A ANALIZAR:
            {datos_analisis}
            """
            
            # Llamada al modelo con Streaming
            stream = client.models.generate_content_stream(
                model='gemini-3.5-flash',
                contents=prompt
            )
            
            st.subheader("📋 Diagnóstico Técnico:")
            res_container = st.empty()
            full_text = ""
            
            for chunk in stream:
                if chunk.text:
                    full_text += chunk.text
                    # Actualizamos el contenedor en cada fragmento
                    res_container.markdown(full_text + "▌")
            
            # Limpiamos el cursor al final
            res_container.markdown(full_text)
            
        except Exception as e:
            st.error(f"Ocurrió un error al conectar con la IA: {e}")
            st.write("💡 Sugerencias: Verifica tu API Key, conexión a internet o intenta de nuevo.")

# PIE DE PAGINA
st.divider()
st.caption("Developed by Santiago Cañón Cuervo | AI-powered troubleshooting tool")