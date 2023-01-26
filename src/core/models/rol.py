from src.core.database import db

roles_permisos = db.Table('roles_permisos',
        db.metadata,
        db.Column('rol_id', db.Integer, db.ForeignKey('roles.id')),
        db.Column('permiso_id', db.Integer, db.ForeignKey('permisos.id'))
        )

class Rol(db.Model):
    __tablename__ = 'roles'

    id      = db.Column(db.Integer, primary_key = True)
    name    = db.Column(db.String(255),)
    #personal= db.relationship('Personal')

    permisos = db.relationship('Permiso', secondary=roles_permisos, backref='roles')
    #disciplinas = db.relationship('Disciplina', secondary=socio_disciplina, backref='roles')


    def __init__(self, name=None):
        self.name = name