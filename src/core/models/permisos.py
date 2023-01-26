from src.core.database import db

class Permiso(db.Model):
    __tablename__ = 'permisos'

    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(255))

    def __init__(self, name=None):
        self.name = name
