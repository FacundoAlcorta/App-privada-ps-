from datetime import datetime
#from src.core.models.socio_disciplina import socio_discipliona
from xml.dom.expatbuilder import DOCUMENT_NODE
from src.core.database import db

socio_disciplina = db.Table('socio_disciplina',
        db.metadata,
        db.Column('socio_id', db.Integer, db.ForeignKey('socios.id')),
        db.Column('disciplina_id', db.Integer, db.ForeignKey('disciplinas.id'))
        )


class Socio(db.Model):
    __tablename__ = "socios"

    id              = db.Column(db.Integer, primary_key=True)
    nombre          = db.Column(db.String(255), nullable=False)
    apellido        = db.Column(db.String(255), nullable=False)
    fecha_inicio    = db.Column(db.DateTime, default=datetime.now())
    eliminado       = db.Column(db.Boolean(), default=False)
    password        = db.Column(db.String(100))

    #bloqueado       = db.Column(db.Boolean(), default=False)
    tipo_documento  = db.Column(db.String(255), nullable=False)  # select
    documento       = db.Column(db.Integer())                         # select
    genero          = db.Column(db.String(255), nullable=False)
    #nro_socio       = db.Column(db.Integer(), primary_key=True)                         # HACER AUTO GENERATE
    direccion       = db.Column(db.String(255), nullable=False)
    estado          = db.Column(db.Boolean(), nullable= True, default=False)            # activo/no activo
    telefono        = db.Column(db.String(255), nullable=True)         # optional
    email           = db.Column(db.String(255), nullable=True)     # optional

    moroso          = db.Column(db.Boolean(), default=False)
    disciplinas     = db.relationship('Disciplina', secondary=socio_disciplina, backref='socios')



    # creado_en       = db.Column(db.DateTime, default=datetime.now())
    # modificado_en   = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __init__(self,nombre, apellido, password,tipo_documento,documento,genero,direccion,telefono,email):
        self.nombre = nombre
        self.apellido = apellido
        self.password = password
        self.tipo_documento = tipo_documento
        self.documento = documento
        self.genero = genero
        self.direccion = direccion
        self.telefono = telefono
        self.email = email

    def __repr__(self):
        return f"Socio(id={self.id!r}, documento={self.documento!r})"

        


