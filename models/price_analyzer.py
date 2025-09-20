import json
import random
from datetime import datetime, timedelta

class PriceAnalyzer:
    def __init__(self):
        with open('data/productos_mercado.json', 'r', encoding='utf-8') as f:
            self.productos_data = json.load(f)
    
    def obtener_precios_actuales(self):
        """Simula precios actuales con variaciones aleatorias"""
        precios = {}
        
        for producto_id, data in self.productos_data['productos'].items():
            precios[producto_id] = {
                'nombre': data['nombre'],
                'unidad': data['unidad'],
                'mercados': {}
            }
            
            for mercado, info in data['mercados'].items():
                # Simular variación de precio
                precio_base = info['precio']
                variacion = random.uniform(-0.1, 0.1)  # ±10%
                precio_actual = int(precio_base * (1 + variacion))
                
                precios[producto_id]['mercados'][mercado] = {
                    'precio': precio_actual,
                    'variacion': round(variacion * 100, 1)
                }
        
        return precios
    
    def generar_historico(self, producto, dias=30):
        """Genera datos históricos simulados"""
        if producto not in self.productos_data['productos']:
            return None
        
        precio_base = self.productos_data['productos'][producto]['mercados']['corabastos']['precio']
        historico = []
        
        for i in range(dias):
            fecha = datetime.now() - timedelta(days=dias-i)
            # Simular variación histórica
            variacion = random.uniform(-0.15, 0.15)
            precio = int(precio_base * (1 + variacion))
            
            historico.append({
                'fecha': fecha.strftime('%Y-%m-%d'),
                'precio': precio
            })
        
        return historico
    
    def calcular_tendencia(self, historico):
        """Calcula tendencia de precios"""
        if len(historico) < 7:
            return "insuficiente_data"
        
        precios_recientes = [h['precio'] for h in historico[-7:]]
        precios_anteriores = [h['precio'] for h in historico[-14:-7]]
        
        promedio_reciente = sum(precios_recientes) / len(precios_recientes)
        promedio_anterior = sum(precios_anteriores) / len(precios_anteriores)
        
        cambio = (promedio_reciente - promedio_anterior) / promedio_anterior
        
        if cambio > 0.05:
            return "alza"
        elif cambio < -0.05:
            return "baja"
        else:
            return "estable"
    
    def generar_recomendacion_venta(self, producto):
        """Genera recomendación de venta"""
        historico = self.generar_historico(producto)
        tendencia = self.calcular_tendencia(historico)
        
        recomendaciones = {
            "alza": {
                "mensaje": "📈 Buen momento para vender - precios al alza",
                "color": "success",
                "icono": "📈"
            },
            "baja": {
                "mensaje": "📉 Considera esperar - precios en baja",
                "color": "warning"
            }
        }
        return recomendaciones.get(tendencia)