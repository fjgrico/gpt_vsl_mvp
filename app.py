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
    with st.spinner("Generando guion…"):
        prompt = f"""
        Eres un copywriter profesional, experto en Video Sales Letters.
        Tu tarea: generar un guion completo de VSL en ESPAÑOL de **entre 600 y 800 palabras** (≈4,5‑6,5 min de lectura en voz alta; nunca sobrepases 7 min).
        Usa un tono **formal, profesional y cercano**, que inspire confianza, con lenguaje llano, sin tecnicismos.

        ### Estructura obligatoria:
        1. Hook inicial impactante.
        2. Historia personal breve.
        3. Exposición del dolor/problema.
        4. Presentación del producto/servicio.
        5. Beneficios principales.
        6. Testimonios.
        7. Objeciones + rebatidas.
        8. Garantía ofrecida.
        9. Llamada a la acción.

        ### Datos para personalizar:
        - Producto: {nombre_producto}
        - Público: {publico_objetivo}
        - Problema: {dolor_problema}
        - Beneficios: {beneficios_clave}
        - Precio: {precio_forma_pago}
        - Garantía: {garantia}
        - CTA: {cta}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres experto en VSL."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=900,
                temperature=0.7
            )
            guion = response.choices[0].message.content

            st.subheader("Guion generado")
            st.markdown(guion)

            # ⬇️ AQUÍ EMPIEZA EL BLOQUE CORREGIDO PARA PDF
            from fpdf import FPDF
            import base64

            # Función para crear PDF del guion
            def crear_pdf(texto):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                lineas = texto.split('\n')
                for linea in lineas:
                    pdf.multi_cell(0, 10, txt=linea.encode('latin-1', 'replace').decode('latin-1'))
                return pdf.output(dest='S').encode('latin-1')

            # Genera PDF
            pdf_data = crear_pdf(guion)
            b64 = base64.b64encode(pdf_data).decode('latin-1')
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="guion_vsl.pdf">📥 Descargar Guion en PDF</a>'
            st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
