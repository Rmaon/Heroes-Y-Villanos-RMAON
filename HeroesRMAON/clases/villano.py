import random
from clases.persona import Persona


class Villano(Persona):
    def __init__(self, nombre, apellidos, fecha_nacimiento, identificador=None, puntuacion_total=None,
                 chagepeteador=None, entregador_tardio=None, ausencias=None, hablador=None):
        super().__init__(nombre, apellidos, fecha_nacimiento, identificador=identificador,
                         puntuacion_total=0 if puntuacion_total is None else puntuacion_total)
        self.chagepeteador = chagepeteador if chagepeteador is not None else random.randint(0, 100)
        self.entregador_tardio = entregador_tardio if entregador_tardio is not None else random.randint(0, 100)
        self.ausencias = ausencias if ausencias is not None else random.randint(0, 100)
        self.hablador = hablador if hablador is not None else random.randint(0, 100)
        if puntuacion_total is None:
            self.puntuacion_total = sum([
                self.chagepeteador,
                self.entregador_tardio,
                self.ausencias,
                self.hablador
            ])

    def to_dict(self):
        base = super().to_dict()
        base.update({
            'chagepeteador': self.chagepeteador,
            'entregador_tardio': self.entregador_tardio,
            'ausencias': self.ausencias,
            'hablador': self.hablador
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
            chagepeteador=data.get('chagepeteador'),
            entregador_tardio=data.get('entregador_tardio'),
            ausencias=data.get('ausencias'),
            hablador=data.get('hablador')
        )

    def to_string(self):
        parts = [
            f"Nombre: {self.nombre} {self.apellidos}",
            f"Fecha nacimiento: {self.fecha_nacimiento}",
            f"Puntuación total: {self.puntuacion_total}",
            f"Chagepeteador: {self.chagepeteador}",
            f"Entregador Tardío: {self.entregador_tardio}",
            f"Ausencias: {self.ausencias}",
            f"Hablador: {self.hablador}"
        ]
        return ' | '.join(parts)

    def __str__(self):
        return self.to_string()