from enum import Enum 
class TypeSensor(Enum):
    AGUA = 'Agua'
    AIRE = 'Aire'
    
    @property
    def serialize(self):
        return {
            'name': self.value  # Usa .value para obtener el valor del Enum
        } 

    @classmethod
    def all_types(cls):
        return [sensor.serialize for sensor in cls]
