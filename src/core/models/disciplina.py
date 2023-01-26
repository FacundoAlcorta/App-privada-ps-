from datetime import datetime
from src.core.database import db

class Disciplina(db.Model):      
    __tablename__ = "disciplinas"

    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(100))
    categoria   = db.Column(db.String(100))
    dias = db.Column(db.String(255))
    horario = db.Column(db.String(255))
    costo_mensual = db.Column(db.Integer())                     # debe estar en pesos y si se quiere mostrar en usd que se multiplique desp
    instructores = db.Column(db.String(100))
    estado = db.Column(db.Boolean(), default=False)             # habilitado o no
    #creado_en = db.Column(db.DateTime, default=datetime.now())
    #modificado_en = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    eliminado = db.Column(db.Boolean(), default=False)

    def __init__(self, nombre, categoria, dias, horario, costo_mensual, instructores):
        self.nombre = nombre
        self.categoria = categoria
        self.dias = dias
        self.horario = horario
        self.costo_mensual = costo_mensual
        self.instructores = instructores
