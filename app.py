import os
import streamlit as st
import openai
from dotenv import load_dotenv
from fpdf import FPDF
import base64

# --- Configuración ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Generador de Guiones de VSL con IA (5‑7 min)")
st.write("Selecciona tu nicho, rellena los campos y genera un guion profesional.")

# --- Selección de nicho ---
nicho = st.selectbox("Selecciona tu tipo de negocio/nicho:", [
    "Coach", "Terapeuta", "Consultor", "Formador", "Nutricionista",
    "Agencia", "Psicólogo", "Negocio SaaS", "Entrenador personal", "Otro"
])

# --- Inputs personalizados ---
nombre_producto   = st.text_input("Nombre del producto/servicio",           key="nombre_producto")
publico_objetivo  = st.text_input("Público objetivo (Ej: coaches…)",         key="publico_objetivo")
dolor_problema    = st.text_area ("Dolor/Problema principal que resuelve",  key="dolor_problema")
beneficios_clave  = st.text_area ("Beneficios clave (separa con comas)",     key="beneficios_clave")
precio_forma_pago = st.text_input("Precio / Forma de pago",                 key="precio")
garantia          = st.text_input("Garantía ofrecida",                      key="garantia")
cta               = st.text_input("Llamada a la acción (CTA)",              key="cta")

# --- Ejemplos por nicho ---
ejemplos_nicho = {
    "Coach": "Ejemplo: 'Con mi programa de coaching, mis clientes lograron superar bloqueos personales, mejorando su rendimiento profesional y emocional...'",
    "Terapeuta": "Ejemplo: 'A través de la terapia, mis pacientes han reducido drásticamente la ansiedad y el estrés, logrando una vida más equilibrada y feliz...'",
    "Consultor": "Ejemplo: 'Gracias a mis servicios de consultoría, empresas como la tuya aumentaron un 200% su rentabilidad en menos de 12 meses...'",
    "Formador": "Ejemplo: 'Mis formaciones permiten adquirir habilidades prácticas y aplicables desde el primer día, aumentando tu valor profesional...'",
    "Nutricionista": "Ejemplo: 'Con mis planes personalizados, mis clientes lograron perder peso y mejorar notablemente su salud sin pasar hambre...'",
    "Agencia": "Ejemplo: 'Hemos ayudado a nuestros clientes a multiplicar sus ventas gracias a estrategias efectivas de marketing digital...'",
    "Psicólogo": "Ejemplo: 'Mis pacientes recuperaron la tranquilidad y el control de sus vidas, resolviendo problemas profundos con un método probado...'",
    "Negocio SaaS": "Ejemplo: 'Nuestra plataforma permitió a empresas ahorrar cientos de horas mensuales automatizando procesos repetitivos...'",
    "Entrenador personal": "Ejemplo: 'Mis clientes transformaron su cuerpo, ganaron energía y recuperaron su autoestima gracias a un entrenamiento totalmente personalizado...'",
    "Otro": ""
}

# --- Botón de generación ---
if st.button("Generar Guion de VSL", key="btn_generar"):
    with st.spinner("Generando guion…"):
        prompt = f"""
Eres un copywriter profesional, experto en Video Sales Letters.
Genera un guion de VSL en ESPAÑOL de entre 600 y 800 palabras (máx. 7 minutos), formal, profesional y cercano.
Usa lenguaje sencillo, sin tecnicismos.

Nicho seleccionado: {nicho}
{ejemplos_nicho[nicho]}

### Estructura obligatoria:
1. Hook inicial impactante.
2. Historia personal adaptada al nicho.
3. Dolor/problema específico del público.
4. Presentación del producto como solución.
5. Beneficios clave (en bullets).
6. Testimonios específicos (nombre y profesión).
7. Objeciones comunes + rebatidas.
8. Garantía clara.
9. Llamada a la acción final.

### Datos del usuario:
- Producto: {nombre_producto}
- Público objetivo: {publico_objetivo}
- Problema principal: {dolor_problema}
- Beneficios: {beneficios_clave}
- Precio / forma de pago: {precio_forma_pago}
- Garantía ofrecida: {garantia}
- Llamada a la acción: {cta}
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

            st.subheader("Guion generado")
            st.markdown(guion)

            # --- Exportación a PDF ---
            def crear_pdf(texto):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for linea in texto.split('\n'):
                    pdf.multi_cell(0, 10, txt=linea.encode('latin-1', 'replace').decode('latin-1'))
                return pdf.output(dest='S').encode('latin-1')

            pdf_data = crear_pdf(guion)
            b64 = base64.b64encode(pdf_data).decode('latin-1')
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="guion_vsl.pdf">📥 Descargar Guion en PDF</a>'
            st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
