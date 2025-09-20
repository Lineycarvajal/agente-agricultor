from datetime import datetime
import random

class WeatherAnalyzer:
    def __init__(self):
        self.recomendaciones = {
            'riego': {
                'lluvia': "❌ No riegues hoy, hay lluvia prevista",
                'despejado': "✅ Buen día para regar, no hay lluvia en 48h",
                'nublado': "⚠️ Puedes regar, pero vigila el pronóstico"
            },
            'fertilizacion': {
                'lluvia': "❌ Evita fertilizar, la lluvia puede lavar los nutrientes",
                'despejado': "✅ Excelente día para fertilizar",
                'nublado': "✅ Buen día para fertilizar"
            },
            'fumigacion': {
                'lluvia': "❌ No fumigues, la lluvia reducirá la efectividad",
                'despejado': "✅ Ideal para fumigar, sin viento fuerte",
                'nublado': "✅ Buen día para fumigar"
            }
        }
    
    def generar_recomendaciones(self, clima_data, cultivo="general"):
        """Genera recomendaciones basadas en el clima"""
        condicion = clima_data['weather'][0]['main'].lower()
        
        if 'rain' in condicion:
            estado_clima = 'lluvia'
        elif 'clear' in condicion:
            estado_clima = 'despejado'
        else:
            estado_clima = 'nublado'
        
        recomendaciones = []
        
        for actividad, consejos in self.recomendaciones.items():
            recomendaciones.append({
                'actividad': actividad.title(),
                'consejo': consejos[estado_clima],
                'prioridad': self.calcular_prioridad(actividad, estado_clima)
            })
        
        return sorted(recomendaciones, key=lambda x: x['prioridad'], reverse=True)
    
    def calcular_prioridad(self, actividad, clima):
        """Calcula prioridad de la recomendación"""
        prioridades = {
            ('riego', 'lluvia'): 1,
            ('riego', 'despejado'): 3,
            ('fertilizacion', 'despejado'): 2,
            ('fumigacion', 'despejado'): 2
        }
        
        return prioridades.get((actividad, clima), 1)
    
    def generar_alertas(self, pronostico_data):
        """Genera alertas basadas en el pronóstico"""
        alertas = []
        
        for dia in pronostico_data['list'][:3]:  # Próximos 3 días
            temp_max = dia['main']['temp_max']
            condicion = dia['weather'][0]['main']
            fecha = dia['dt_txt']
            
            if temp_max > 30:
                alertas.append({
                    'tipo': 'temperatura',
                    'mensaje': f"🌡️ Alerta: Temperatura alta ({temp_max}°C) el {fecha[:10]}",
                    'nivel': 'warning'
                })
            
            if 'rain' in condicion.lower():
                alertas.append({
                    'tipo': 'lluvia',
                    'mensaje': f"🌧️ Lluvia prevista para el {fecha[:10]}",
                    'nivel': 'info'
                })
        
        return alertas