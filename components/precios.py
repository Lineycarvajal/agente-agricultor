import streamlit as st
from models.price_analyzer import PriceAnalyzer
import plotly.graph_objects as go

def mostrar_precios():
    st.header("💰 Precios de Mercado")
    
    analyzer = PriceAnalyzer()
    
    # Obtener precios actuales
    precios_actuales = analyzer.obtener_precios_actuales()
    
    # Selección de producto
    producto_seleccionado = st.selectbox(
        "Selecciona un producto:",
        options=list(precios_actuales.keys()),
        format_func=lambda x: precios_actuales[x]['nombre']
    )
    
    if producto_seleccionado:
        mostrar_info_producto(producto_seleccionado, precios_actuales, analyzer)

def mostrar_info_producto(producto_id, precios, analyzer):
    """Muestra información detallada de un producto"""
    producto = precios[producto_id]
    
    st.subheader(f"📊 {producto['nombre']} ({producto['unidad']})")
    
    # Mostrar precios en diferentes mercados
    st.markdown("---")
    st.write("#### Precios Actuales por Mercado")
    
    cols = st.columns(len(producto['mercados']))
    
    for i, (mercado, data) in enumerate(producto['mercados'].items()):
        with cols[i]:
            delta = f"{data['variacion']}%"
            st.metric(
                label=mercado.title(),
                value=f"${data['precio']:,}",
                delta=delta
            )
    
    # Histórico y tendencia
    st.markdown("---")
    st.write("#### Histórico y Tendencia (últimos 30 días)")
    
    historico = analyzer.generar_historico(producto_id)
    
    if historico:
        # Gráfico de histórico
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[h['fecha'] for h in historico],
            y=[h['precio'] for h in historico],
            mode='lines+markers',
            name='Precio Histórico'
        ))
        fig.update_layout(
            title=f"Histórico de Precios para {producto['nombre']}",
            xaxis_title="Fecha",
            yaxis_title="Precio"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Recomendación de venta
        recomendacion = analyzer.generar_recomendacion_venta(producto_id)
        if recomendacion:
            st.subheader("💡 Recomendación de Venta")
            if recomendacion['color'] == 'success':
                st.success(f"{recomendacion['icono']} {recomendacion['mensaje']}")
            else:
                st.warning(f"{recomendacion['icono']} {recomendacion['mensaje']}")