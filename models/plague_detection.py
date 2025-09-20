import json
import random
from PIL import Image
import numpy as np

class PlagueDetector:
    def __init__(self):
        with open('data/plagues_db.json', 'r', encoding='utf-8') as f:
            self.plagas_db = json.load(f)
    
    def analizar_imagen(self, imagen):
        """Simula análisis de imagen con IA"""
        # Simulación mejorada: selecciona aleatoriamente solo plagas del café
        plagas_cafe = [id for id, detalles in self.plagas_db['plagas'].items()
                       if "cafe" in detalles.get("cultivos_afectados", [])]
        
        if not plagas_cafe:
            # Fallback por si no hay plagas de café definidas
            plagas_cafe = list(self.plagas_db['plagas'].keys())

        plaga_detectada = random.choice(plagas_cafe)
        confianza = random.uniform(0.7, 0.95)
        
        return {
            'plaga_id': plaga_detectada,
            'confianza': confianza,
            'info': self.plagas_db['plagas'][plaga_detectada]
        }
    
    def obtener_tratamientos(self, plaga_id):
        """Retorna tratamientos para una plaga específica"""
        if plaga_id in self.plagas_db['plagas']:
            return self.plagas_db['plagas'][plaga_id]
        return None

def preprocesar_imagen(imagen):
    """Preprocesa imagen para análisis"""
    # Redimensionar imagen
    imagen = imagen.resize((224, 224))
    # Convertir a array numpy
    img_array = np.array(imagen)
    return img_array