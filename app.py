import streamlit as st
from components.chat_interface import interfaz_chat
from components.diagnostico import mostrar_diagnostico
from components.clima import mostrar_clima
from components.precios import mostrar_precios

st.set_page_config(
    page_title="🌱 Asistente de Cultivos",
    page_icon="🌱",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🌱 Asistente de Cultivos Inteligente</h1></div>', 
            unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📱 Navegación")
st.sidebar.markdown("---")
opcion = st.sidebar.selectbox("Selecciona una opción:", 
                             ["💬 Chat", "🔍 Diagnóstico", "🌤️ Clima", "💰 Precios"])

if opcion == "💬 Chat":
    interfaz_chat()
elif opcion == "🔍 Diagnóstico":
    mostrar_diagnostico()
elif opcion == "🌤️ Clima":
    mostrar_clima()
elif opcion == "💰 Precios":
    mostrar_precios()