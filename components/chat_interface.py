import streamlit as st
from datetime import datetime

def mostrar_mensaje(mensaje, es_usuario=True):
    col1, col2, col3 = st.columns([1, 6, 1])
    
    if es_usuario:
        with col3:
            st.markdown(f"""
            <div style='background-color: #DCF8C6; padding: 10px; 
                        border-radius: 10px; margin: 5px;'>
                {mensaje}
            </div>
            """, unsafe_allow_html=True)
    else:
        with col1:
            st.markdown("🤖")
        with col2:
            st.markdown(f"""
            <div style='background-color: #F1F1F1; padding: 10px; 
                        border-radius: 10px; margin: 5px;'>
                {mensaje}
            </div>
            """, unsafe_allow_html=True)

def interfaz_chat():
    st.subheader("💬 Chat con tu Asistente Agrícola")
    
    # Inicializar historial de chat
    if 'mensajes' not in st.session_state:
        st.session_state.mensajes = [
            {"mensaje": "¡Hola! Soy tu asistente agrícola. ¿En qué puedo ayudarte?", 
             "es_usuario": False}
        ]
    
    # Mostrar mensajes
    for msg in st.session_state.mensajes:
        mostrar_mensaje(msg["mensaje"], msg["es_usuario"])
    
    # Input de usuario
    user_input = st.text_input("Escribe tu consulta:", key="chat_input")
    if st.button("Enviar") and user_input:
        # Agregar mensaje del usuario
        st.session_state.mensajes.append({
            "mensaje": user_input, 
            "es_usuario": True
        })
        
        # Respuesta básica del bot
        respuesta = procesar_consulta(user_input)
        st.session_state.mensajes.append({
            "mensaje": respuesta, 
            "es_usuario": False
        })
        st.rerun()

def procesar_consulta(consulta):
    # Lógica básica de respuestas
    consulta = consulta.lower()
    
    if "clima" in consulta or "tiempo" in consulta:
        return "🌤️ Para consultas del clima, ve a la sección Clima en el menú."
    elif "plaga" in consulta or "enfermedad" in consulta:
        return "🔍 Para diagnóstico de plagas, ve a la sección Diagnóstico."
    elif "precio" in consulta or "mercado" in consulta:
        return "💰 Para precios de mercado, ve a la sección Precios."
    else:
        return "Entiendo tu consulta. Selecciona la opción adecuada del menú para ayudarte mejor."