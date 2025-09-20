import streamlit as st
from models.plague_detection import PlagueDetector, preprocesar_imagen
from PIL import Image

def mostrar_diagnostico():
    st.header("🔍 Diagnóstico de Plagas")
    st.write("Sube una foto de tu cultivo para identificar posibles plagas")
    
    detector = PlagueDetector()
    
    # Upload de imagen
    uploaded_file = st.file_uploader(
        "Selecciona una imagen", 
        type=['png', 'jpg', 'jpeg'],
        help="Sube una foto clara de la hoja o fruto afectado"
    )
    
    if uploaded_file is not None:
        # Mostrar imagen
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Imagen subida", use_column_width=True)
        
        with col2:
            if st.button("🔍 Analizar Imagen", type="primary"):
                with st.spinner('Analizando imagen...'):
                    # Simular tiempo de procesamiento
                    import time
                    time.sleep(2)
                    
                    # Procesar imagen
                    img_procesada = preprocesar_imagen(image)
                    resultado = detector.analizar_imagen(img_procesada)
                    
                    # Mostrar resultados
                    mostrar_resultados(resultado)

def mostrar_resultados(resultado):
    """Muestra los resultados del diagnóstico"""
    st.success("✅ Análisis completado")
    
    # Información de la plaga
    info = resultado['info']
    confianza = resultado['confianza']
    
    # Métrica de confianza
    st.metric("Confianza del diagnóstico", f"{confianza:.1%}")
    
    # Información de la plaga
    st.subheader(f"🐛 {info['nombre']}")
    st.write(info['descripcion'])
    
    # Síntomas
    st.subheader("🔍 Síntomas identificados:")
    for sintoma in info['sintomas']:
        st.write(f"• {sintoma}")
    
    # Tratamientos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌿 Tratamiento Orgánico")
        st.success(info['tratamiento_organico'])
    
    with col2:
        st.subheader("⚗️ Tratamiento Químico")
        st.warning(info['tratamiento_quimico'])
    
    # Cultivos afectados
    st.subheader("🌾 Cultivos comúnmente afectados:")
    cultivos = ", ".join(info['cultivos_afectados']).title()
    st.info(f"📋 {cultivos}")