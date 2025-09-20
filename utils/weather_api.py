import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class WeatherAPI:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY', 'demo_key')
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def obtener_clima_actual(self, ciudad="Bogotá"):
        """Obtiene el clima actual para una ciudad"""
        if self.api_key == 'demo_key':
            return self.simular_clima_actual()
        
        url = f"{self.base_url}/weather"
        params = {
            'q': ciudad,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'es'
        }
        
        try:
            response = requests.get(url, params=params)
            return response.json()
        except:
            return self.simular_clima_actual()
    
    def obtener_pronostico(self, ciudad="Bogotá"):
        """Obtiene pronóstico de 5 días"""
        if self.api_key == 'demo_key':
            return self.simular_pronostico()
        
        url = f"{self.base_url}/forecast"
        params = {
            'q': ciudad,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'es'
        }
        
        try:
            response = requests.get(url, params=params)
            return response.json()
        except:
            return self.simular_pronostico()
    
    def simular_clima_actual(self):
        """Simula datos de clima para demo"""
        import random
        return {
            'main': {
                'temp': random.randint(18, 28),
                'humidity': random.randint(60, 90),
                'pressure': random.randint(1010, 1020)
            },
            'weather': [
                {
                    'main': random.choice(['Rain', 'Clouds', 'Clear']),
                    'description': random.choice(['lluvia ligera', 'nublado', 'despejado'])
                }
            ],
            'wind': {
                'speed': random.uniform(2, 8)
            }
        }
    
    def simular_pronostico(self):
        """Simula pronóstico para demo"""
        import random
        pronostico = []
        
        for i in range(5):
            fecha = datetime.now() + timedelta(days=i)
            pronostico.append({
                'dt_txt': fecha.strftime('%Y-%m-%d 12:00:00'),
                'main': {
                    'temp_max': random.randint(20, 30),
                    'temp_min': random.randint(15, 20),
                    'humidity': random.randint(60, 90)
                },
                'weather': [
                    {
                        'main': random.choice(['Rain', 'Clouds', 'Clear']),
                        'description': random.choice(['lluvia', 'nublado', 'despejado'])
                    }
                ]
            })
        
        return {'list': pronostico}