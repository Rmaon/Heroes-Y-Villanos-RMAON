import uuid

class Persona:
    def __init__(self, nombre, apellidos, fecha_nacimiento, identificador=None, puntuacion_total=0):
        self.nombre = nombre
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.identificador = identificador or str(uuid.uuid4())
        self.puntuacion_total = puntuacion_total

    def to_dict(self):
        return {
            'tipo': self.__class__.__name__,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'fecha_nacimiento': self.fecha_nacimiento,
            'identificador': self.identificador,
            'puntuacion_total': self.puntuacion_total
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('nombre'),
            data.get('apellidos'),
            data.get('fecha_nacimiento'),
            identificador=data.get('identificador'),
            puntuacion_total=data.get('puntuacion_total', 0)
        )