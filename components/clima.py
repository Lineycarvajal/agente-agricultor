import streamlit as st
from utils.weather_api import WeatherAPI
from models.weather_analyzer import WeatherAnalyzer
import plotly.graph_objects as go
from datetime import datetime

def mostrar_clima():
    st.header("🌤️ Información Meteorológica")
    
    # Input de ciudad
    col1, col2 = st.columns([3, 1])
    with col1:
        ciudad = st.text_input("Ciudad:", value="Bogotá", key="ciudad_input")
    with col2:
        actualizar = st.button("🔄 Actualizar", type="primary")
    
    if actualizar or 'clima_data' not in st.session_state:
        with st.spinner('Obteniendo datos meteorológicos...'):
            api_clima = WeatherAPI()
            analyzer = WeatherAnalyzer()
            
            # Obtener datos
            clima_actual = api_clima.obtener_clima_actual(ciudad)
            pronostico = api_clima.obtener_pronostico(ciudad)
            
            # Guardar en session state
            st.session_state.clima_data = {
                'actual': clima_actual,
                'pronostico': pronostico,
                'recomendaciones': analyzer.generar_recomendaciones(clima_actual),
                'alertas': analyzer.generar_alertas(pronostico)
            }
    
    if 'clima_data' in st.session_state:
        data = st.session_state.clima_data
        mostrar_clima_actual(data['actual'])
        mostrar_recomendaciones(data['recomendaciones'])
        mostrar_alertas(data['alertas'])
        mostrar_pronostico(data['pronostico'])

def mostrar_clima_actual(clima_data):
    """Muestra el clima actual"""
    st.subheader("🌡️ Clima Actual")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Temperatura", f"{clima_data['main']['temp']}°C")
    with col2:
        st.metric("Humedad", f"{clima_data['main']['humidity']}%")
    with col3:
        st.metric("Viento", f"{clima_data['wind']['speed']} km/h")
    with col4:
        st.metric("Condición", clima_data['weather'][0]['description'].title())

def mostrar_recomendaciones(recomendaciones):
    """Muestra recomendaciones agrícolas"""
    st.subheader("💡 Recomendaciones para Hoy")
    
    for rec in recomendaciones:
        if rec['prioridad'] >= 2:
            st.success(f"**{rec['actividad']}:** {rec['consejo']}")
        else:
            st.info(f"**{rec['actividad']}:** {rec['consejo']}")

def mostrar_alertas(alertas):
    """Muestra alertas meteorológicas"""
    if alertas:
        st.subheader("⚠️ Alertas")
        for alerta in alertas:
            if alerta['nivel'] == 'warning':
                st.warning(alerta['mensaje'])
            else:
                st.info(alerta['mensaje'])

def mostrar_pronostico(pronostico_data):
    """Muestra pronóstico de 5 días"""
    st.subheader("📅 Pronóstico 5 Días")
    
    fechas = []
    temps_max = []
    temps_min = []
    
    for dia in pronostico_data['list'][:5]:
        fechas.append(dia['dt_txt'][:10])
        temps_max.append(dia['main']['temp_max'])
        temps_min.append(dia['main']['temp_min'])
    
    # Crear gráfico con Plotly
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=fechas, y=temps_max,
        mode='lines+markers',
        name='Máxima',
        line=dict(color='red')
    ))
    
    fig.add_trace(go.Scatter(
        x=fechas, y=temps_min,
        mode='lines+markers',
        name='Mínima',
        line=dict(color='blue')
    ))
    
    fig.update_layout(
        title="Temperaturas Próximos 5 Días",
        xaxis_title="Fecha",
        yaxis_title="Temperatura (°C)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)