from collections import UserList
from email.policy import default
from enum import unique
from src.core.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



class Personal(db.Model):     
                                         # MODIFICAR TAMAÑOS DE STR
    __tablename__ = "personal"
    id              = db.Column(db.Integer, primary_key=True)
    nombre          = db.Column(db.String(255), nullable=False)
    apellido        = db.Column(db.String(255), nullable=False)
    email           = db.Column(db.String(255))
    password        = db.Column(db.String(100))

    eliminado       = db.Column(db.Boolean(), default=False)
    bloqueado       = db.Column(db.Boolean(), default=False)

    fecha_inicio    = db.Column(db.DateTime, default=datetime.now())
    ### CONSULTAR
    rol_id          = db.Column(db.Integer, default=1)  #db.Column(db.Integer, db.ForeignKey('roles.id'))


    def __init__(self,nombre,apellido,email,password, rol_id):
        self.nombre = nombre
        self.apellido = apellido
        self.password = password
        self.email = email
        self.rol_id = rol_id
    
    def __repr__(self):
        return f"Personal(id={self.id!r}, email={self.email!r})"
