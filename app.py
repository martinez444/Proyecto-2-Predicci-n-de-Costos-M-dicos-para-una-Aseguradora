import numpy as np
import pandas as pd
import requests  # Librería para conectar la interfaz con el backend de IA
import streamlit as st

# ==========================================
# CONFIGURACIÓN GENERAL DE LA PÁGINA WEB
# ==========================================
# Configuramos la pestaña del navegador, icono y el diseño de pantalla ancha (wide)
st.set_page_config(
    page_title="SaludMás Seguros",
    page_icon="🏥",
    layout="wide",
)

# ==========================================
# ENCABEZADO Y DISEÑO VISUAL LLAMATIVO
# ==========================================
# Creamos dos columnas en la cabecera: una para la imagen representativa y otra para el título institucional
col_banner_izq, col_banner_der = st.columns([2, 1], gap="medium")

with col_banner_izq:
    st.markdown("""
        <div style="background-color:#0f172a; padding:25px; border-radius:12px; color:white; text-align:left; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="margin:0; color:#38bdf8;">🏥 SaludMás Seguros S.A.</h1>
            <p style="margin:10px 0 0 0; font-size:1.15em; color:#e2e8f0;">
                Plataforma Inteligente de Estimación de Costes Médicos y Pólizas de Salud en España.
        
        </div>
    """, unsafe_allow_html=True)

with col_banner_der:
    # Imagen representativa de salud/seguros de alta calidad (Cargada directamente desde URL segura)
    st.image(
        "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=600&q=80",
        caption="Atención Médica y Bienestar",
        use_container_width=True
    )

st.write("")  # Espaciador vertical

# ==========================================
# PANEL LATERAL: CAPTURA DE DATOS DEL CLIENTE
# ==========================================
st.sidebar.header("📋 Perfil del Asegurado")
st.sidebar.markdown("Introduzca los parámetros médicos y demográficos:")

# Controles interactivos con rangos lógicos para cada variable del modelo
edad = st.sidebar.slider("Edad (Años)", 18, 65, 30)
sexo = st.sidebar.selectbox("Sexo biológico", ["femenino", "masculino"])
imc = st.sidebar.number_input("Índice de Masa Corporal (IMC)", 16.0, 50.0, 25.0, 0.1)
hijos = st.sidebar.slider("Número de Hijos / Dependientes", 0, 5, 0)
region = st.sidebar.selectbox("Región de residencia", ["norte", "sur", "este", "oeste"])
fumador = st.sidebar.selectbox("¿Es fumador activo?", ["no", "sí"])

# Empaquetamos los datos ingresados en un DataFrame de una sola fila
df_cliente = pd.DataFrame({
    'edad': [edad],
    'sexo': [sexo],
    'imc': [imc],
    'hijos': [hijos],
    'region': [region],
    'fumador': [fumador]
})

# ==========================================
# PANTALLA PRINCIPAL: DISEÑO EN DOS COLUMNAS
# ==========================================
col_izquierda, col_derecha = st.columns([1, 1], gap="large")

with col_izquierda:
    st.subheader("🔍 Resumen de Datos Ingresados")
    # Mostramos la tabla del cliente adaptada al ancho de la columna
    st.dataframe(df_cliente, use_container_width=True, hide_index=True)
    
    # Validación clínica rápida del IMC según los estándares médicos de la OMS
    if imc < 18.5:
        st.info("ℹ️ **Estado Nutricional:** Bajo peso")
    elif 18.5 <= imc < 25.0:
        st.success("✅ **Estado Nutricional:** Peso saludable (Normal)")
    elif 25.0 <= imc < 30.0:
        st.warning("⚠️ **Estado Nutricional:** Sobrepeso")
    else:
        st.error("🚨 **Estado Nutricional:** Obesidad (Factor de riesgo elevado)")


with col_derecha:
    st.subheader("💶 Estimación de la Póliza en Euros")
    
    # Botón principal estilizado para ejecutar el cálculo
    if st.button("🚀 Calcular Cotización Anual con IA", use_container_width=True):
        
        # Diccionario con los datos listos para ser enviados al backend
        datos_envio = {
            "edad": int(edad),
            "sexo": str(sexo),
            "imc": float(imc),
            "hijos": int(hijos),
            "region": str(region),
            "fumador": str(fumador)
        }
        
        try:
            # Intentamos conectar con la API backend de Machine Learning
            respuesta = requests.post("http://127.0.0.1:8000/calcular-costo", json=datos_envio)
            
            if respuesta.status_code == 200:
                coste_estimado = respuesta.json()["costo_medico_anual"]
            else:
                # Sistema de respaldo (Fallback) matemático en caso de error en el servidor
                coste_estimado = 3000.0 + (edad ** 1.35) * 45.0
                
        except Exception:
            # Fórmula de contingencia en euros si el backend está apagado
            coste_estimado = 3000.0 + (edad ** 1.35) * 45.0
            if fumador == 'sí':
                coste_estimado += 14000.0
        
        # Redondeo estricto del coste a dos decimales profesionales
        coste_redondeado = round(max(coste_estimado, 1100.0), 2)
        
        # Renderizamos la métrica destacada en formato de moneda europea (ej. 1.500,00 €)
        st.metric(
            label="Coste Médico Anual Estimado",
            value=f"{coste_redondeado:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        
        # Retroalimentación clínica personalizada según los hábitos del cliente
        if fumador == 'sí':
            st.warning("💡 *Nota clínica:* El consumo de tabaco activo incrementa considerablemente la prima anual en España.")
        else:
            st.success("🌟 ¡Enhorabuena! Mantener hábitos de vida saludables permite acceder a primas reducidas.")
    else:
        st.info("👉 Haga clic en el botón superior para generar el cálculo de la póliza en tiempo real.")

# Pie de página institucional
st.markdown("---")
st.markdown('<p style="text-align: center; color: #64748b; font-size: 0.85em;">2026 | SaludMás Seguros S.A. (España) - Entorno Clínico Inteligente</p>', unsafe_allow_html=True)












