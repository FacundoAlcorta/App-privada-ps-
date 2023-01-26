from src.core.database import db

class Configuracion(db.Model):
    __tablename__ = 'configuracion'

    id                  = db.Column(db.Integer, primary_key=True)
    paginacion          = db.Column(db.Integer)
    monto_base          = db.Column(db.Integer())
    porcentaje_recargo  = db.Column(db.Integer())
    # habilitar tablas publicas (?
    # info contacto (?
    # encabezado recibo de pago

    def __init__ (self, paginacion, monto_base, porcentaje_recargo):
        self.paginacion=paginacion
        self.monto_base=monto_base
        self.porcentaje_recargo=porcentaje_recargo