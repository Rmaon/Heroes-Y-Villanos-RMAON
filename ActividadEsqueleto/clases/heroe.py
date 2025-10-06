import random
from clases.persona import Persona

class Heroe(Persona):
    def __init__(self, nombre, apellidos, fecha_nacimiento, identificador=None, puntuacion_total=None,
                 codigo_limpio=None, bien_documentado=None, gitgod=None, arquitecto=None, detallista=None):
        super().__init__(nombre, apellidos, fecha_nacimiento, identificador=identificador,
                         puntuacion_total=0 if puntuacion_total is None else puntuacion_total)
        self.codigo_limpio = codigo_limpio if codigo_limpio is not None else random.randint(0, 100)
        self.bien_documentado = bien_documentado if bien_documentado is not None else random.randint(0, 100)
        self.gitgod = gitgod if gitgod is not None else random.randint(0, 100)
        self.arquitecto = arquitecto if arquitecto is not None else random.randint(0, 100)
        self.detallista = detallista if detallista is not None else random.randint(0, 100)
        # calcular puntuación si no viene dada
        if puntuacion_total is None:
            self.puntuacion_total = sum([
                self.codigo_limpio,
                self.bien_documentado,
                self.gitgod,
                self.arquitecto,
                self.detallista
            ])

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'codigo_limpio': self.codigo_limpio,
            'bien_documentado': self.bien_documentado,
            'gitgod': self.gitgod,
            'arquitecto': self.arquitecto,
            'detallista': self.detallista
        })
        return base

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('nombre'),
            data.get('apellidos'),
            data.get('fecha_nacimiento'),
            identificador=data.get('identificador'),
            puntuacion_total=data.get('puntuacion_total'),
            codigo_limpio=data.get('codigo_limpio'),
            bien_documentado=data.get('bien_documentado'),
            gitgod=data.get('gitgod'),
            arquitecto=data.get('arquitecto'),
            detallista=data.get('detallista')
        )