from datetime import datetime
from src.core.database import db

class Cuota(db.Model):
    __tablename__   = "cuotas"
    id              = db.Column(db.Integer, primary_key=True)
    monto           = db.Column(db.Integer())
    anomes          = db.Column(db.DateTime, default=datetime.now())    # año y mes de la cuota
    estado_pago     = db.Column(db.Boolean(), default=False)            # indica si se pago esa cuota o no
    creado_en       = db.Column(db.DateTime, default=datetime.now())
    pagado_en       = db.Column(db.DateTime, default=None)
    socio_id        = db.Column(db.Integer)
    flagAumento     = db.Column(db.Boolean(), default=False)            # indica si se aumento la cuota


    def __init__(self, monto, socio_id):
        self.monto=monto
        self.socio_id=socio_id