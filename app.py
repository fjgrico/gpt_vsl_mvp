import os
import streamlit as st
import openai
from dotenv import load_dotenv

# --- Configuración y API KEY ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Título y descripción ---
st.title("Generador de Guiones de VSL con IA (5‑7 min)")
st.write("Rellena los campos y obtén un guion profesional listo para grabar.")

# --- Inputs ---
nombre_producto   = st.text_input("Nombre del producto/servicio",           key="nombre_producto")
publico_objetivo  = st.text_input("Público objetivo (Ej: coaches…)",         key="publico_objetivo")
dolor_problema    = st.text_area ("Dolor/Problema principal que resuelve",    key="dolor_problema")
beneficios_clave  = st.text_area ("Beneficios clave (separa con comas)",      key="beneficios_clave")
precio_forma_pago = st.text_input("Precio / Forma de pago",                  key="precio")
garantia          = st.text_input("Garantía ofrecida",                        key="garantia")
cta               = st.text_input("Llamada a la acción (CTA)",               key="cta")

# --- Generar Guion ---
if st.button("Generar Guion de VSL", key="btn_generar"):
from fpdf import FPDF
import base64

# Función para crear PDF del guion
def crear_pdf(texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Dividir texto en líneas y añadir al PDF
    lineas = texto.split('\n')
    for linea in lineas:
        pdf.multi_cell(0, 10, txt=linea.encode('latin-1', 'replace').decode('latin-1'))
    
    return pdf.output(dest='S').encode('latin-1')

# Generar PDF si existe un guion generado
if 'guion' in locals() or 'guion' in globals():
    pdf_data = crear_pdf(guion)
    b64 = base64.b64encode(pdf_data).decode('latin-1')
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="guion_vsl.pdf">📥 Descargar Guion en PDF</a>'
    
    st.markdown(href, unsafe_allow_html=True)

    with st.spinner("Generando guion…"):
        prompt = f"""
Eres un copywriter profesional, experto en Video Sales Letters.
Tu tarea: generar un guion completo de VSL en ESPAÑOL de **entre 600 y 800 palabras** (≈4,5‑6,5 min de lectura en voz alta; nunca sobrepases 7 min).
Usa un tono **formal, profesional y cercano**, que inspire confianza, con lenguaje llano, sin tecnicismos.

### Estructura obligatoria (usa encabezados o separadores):
1. Hook inicial impactante (1‑2 frases).
2. Historia personal breve y relevante (máx. 2 párrafos) que conecte con el dolor.
3. Exposición clara del dolor o problema del público.
4. Presentación del producto/servicio como solución.
5. Beneficios principales (bullet points breves y potentes).
6. Testimonios verosímiles (2‑3 frases cada uno, menciona nombre de pila y profesión).
7. Objeciones típicas + rebatidas convincentes (al menos 3).
8. Garantía ofrecida.
9. Llamada a la acción final fuerte y específica.

### Datos para personalizar el guion:
- Nombre del producto/servicio: {nombre_producto}
- Público objetivo: {publico_objetivo}
- Dolor/Problema principal: {dolor_problema}
- Beneficios clave: {beneficios_clave}
- Precio / forma de pago: {precio_forma_pago}
- Garantía: {garantia}
- Llamada a la acción: {cta}

Respeta la longitud indicada y la estructura. Utiliza párrafos cortos y voz en segunda persona ("tú").
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto copywriter de VSL."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=900,
                temperature=0.7
            )
            guion = response.choices[0].message.content

            # --- Mostrar resultado en un expander con copia y descarga ---
            st.subheader("Guion generado (5‑7 min)")
            with st.expander("▶️ Ver guion completo"):
                st.markdown(guion)

            st.code(guion, language="markdown")  # incluye icono de copiar

            st.download_button(
                label="Descargar como .txt",
                data=guion,
                file_name="guion_vsl.txt",
                mime="text/plain",
                key="download_txt"
            )
            st.download_button(
                label="Descargar como .md",
                data=guion,
                file_name="guion_vsl.md",
                mime="text/markdown",
                key="download_md"
            )

        except Exception as e:
            st.error(f"Ocurrió un error al generar el guion: {e}")
