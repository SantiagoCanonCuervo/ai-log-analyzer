import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# ==========================================
# CONFIGURACION DE LA PAGINA
# ==========================================

st.set_page_config(
    page_title="AI Log Analyzer",
    page_icon="🚀",
    layout="wide"
)

# ==========================================
# API KEY (LOCAL + STREAMLIT CLOUD "AMBOS ESCENARIOS POSIBLES")
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        st.error(
            "❌ No se encontró GEMINI_API_KEY ni en .env ni en Streamlit Secrets."
        )
        st.stop()

# ==========================================
# IA
# ==========================================

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Error al inicializar Gemini: {e}")
    st.stop()

# ==========================================
# INTERFAZ DE USUARIO FINAL
# ==========================================

st.title("🚀 AI Log Analyzer")

st.write("""
Analiza:

- Logs de aplicaciones
- Errores De cualquier lenguaje
- Tracebacks
- Logs Windows
- Logs Linux
- Logs de servidores
- Errores manuales

Utilizando IA para identificar causas raíz y soluciones.
""")


st.subheader("📂 Subir archivos")

uploaded_files = st.file_uploader(
    "Selecciona archivos .log, .txt o .docx",
    type=["log", "txt", "docx"],
    accept_multiple_files=True
)



st.subheader("✍️ Pegar errores manualmente")

error_text = st.text_area(
    "Pega aquí errores, tracebacks o logs",
    height=250,
    placeholder="""
Ejemplo:

Traceback (most recent call last):
  File "main.py", line 15
NameError: variable not defined
"""
)



# ======================================
# TIPOS DE ARCHIVO PERMITIDOS
# ======================================

ALLOWED_EXTENSIONS = [".txt", ".log", ".docx"]

if st.button("🚀 Analizar Logs"):

    datos_analisis = ""

    # ======================================
    # LEER ARCHIVOS PERMITIDOS
    # ======================================

    if uploaded_files:
                    
                    for file in uploaded_files:

                        try:

                            nombre = file.name.lower()

                            # Validar extensiones
                            if not any(nombre.endswith(ext) for ext in ALLOWED_EXTENSIONS):

                                st.warning(
                                    f"⚠️ {file.name} ignorado: tipo de archivo no permitido."
                                )

                                continue

                            # Validar archivo vacío
                            if file.size == 0:
                                MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

                                if file.size > MAX_FILE_SIZE:
                                    st.warning(
                                        f"⚠️ {file.name} excede el tamaño máximo permitido (10 MB)."
                                    )
                                    continue
                                st.warning(
                                    f"⚠️ {file.name} está vacío."
                                )

                                continue

                            # TXT y LOG
                            if nombre.endswith(".txt") or nombre.endswith(".log"):

                                contenido = file.read().decode(
                                    "utf-8",
                                    errors="ignore"
                                )

                            # DOCX
                            elif nombre.endswith(".docx"):

                                from docx import Document
                                import tempfile

                                with tempfile.NamedTemporaryFile(
                                    delete=False,
                                    suffix=".docx"
                                ) as tmp:

                                    tmp.write(file.getvalue())

                                    ruta_temp = tmp.name

                                doc = Document(ruta_temp)

                                contenido = "\n".join(
                                    p.text for p in doc.paragraphs
                                )

                            else:

                                continue

                            # Validar contenido vacío
                            if not contenido.strip():

                                st.warning(
                                    f"⚠️ {file.name} no contiene texto."
                                )

                                continue

                            datos_analisis += f"""

                =================================================
                ARCHIVO: {file.name}
                =================================================

                {contenido}

                """

                        except UnicodeDecodeError:

                            st.warning(
                                f"⚠️ No fue posible decodificar {file.name}."
                            )

                        except Exception as e:

                            st.warning(
                                f"⚠️ Error procesando {file.name}: {e}"
                            )

                    # ======================================
                    # AGREGAR ERROR DE TERMINAL
                    # ======================================

                    if error_text.strip():

                        datos_analisis += f"""

                =================================================
                ERROR TERMINAL
                =================================================

                {error_text}

                """

                    # ======================================
                    # VALIDAR TERMINAL
                    # ======================================

                    if not datos_analisis.strip():

                        st.warning(
                            "⚠️ Debes subir un archivo o escribir un error."
                        )

                    else:

                        try:

                            prompt = f"""
                Actúa como un Staff Software Engineer especializado en:

                - DevOps
                - SRE
                - Backend
                - Cloud Computing
                - Linux
                - Windows Server
                - Bases de datos
                - Observabilidad
                - Troubleshooting
                - QA SENIOR

                Analiza la información entregada.

                OBJETIVOS:

                1. Detectar errores críticos.

                2. Detectar advertencias importantes.

                3. Identificar la causa raíz.

                4. Clasificar severidad:

                - Crítica
                - Alta
                - Media
                - Baja

                5. Crear una tabla:

                | Línea | Severidad | Error | Causa probable |

                6. Explicar técnicamente cada error.

                7. Proponer soluciones concretas.

                8. Si aplica, incluir:

                - comandos Linux
                - comandos Windows
                - PowerShell
                - SQL
                - cambios de código

                9. Generar un resumen ejecutivo.

                INFORMACIÓN A ANALIZAR:

                {datos_analisis}
                """

                            st.subheader("📋 Diagnóstico Técnico")

                            output_container = st.empty()

                            respuesta_completa = ""

                            stream = client.models.generate_content_stream(
                                model="gemini-2.5-flash-lite",
                                contents=prompt
                            )

                            for chunk in stream:

                                if hasattr(chunk, "text") and chunk.text:

                                    respuesta_completa += chunk.text

                                    output_container.markdown(
                                        respuesta_completa + "▌"
                                    )

                            output_container.markdown(
                                respuesta_completa
                            )

                            st.success(
                                "✅ Análisis completado."
                            )

                        except Exception as e:

                            st.error(
                                f"❌ Error al conectar con Gemini:\n\n{e}"
                            )

                            st.info("""
                Posibles causas:

                - API KEY inválida
                - Sin conexión a internet
                - Cuota agotada
                - Modelo incorrecto
                - Error temporal del servicio
                """)


#CREDITOS


st.divider()
st.caption(
                    "Developed by Santiago Cañón Cuervo"
                )
