from src.core.models.cuota import Cuota
from src.core.database import db
from datetime import datetime
from sqlalchemy import extract  


def create_cuota(monto, socio_id):
    #crea cuota
    cuota = Cuota(monto, socio_id)
    db.session.add(cuota)
    db.session.commit()
    return cuota

def aumento_por_atraso(id, monto):
    #actualiza monto
    cuota = Cuota.query.get(id)
    cuota.monto = monto
    cuota.flagAumento = True
    db.session.commit()
    return cuota


def pago_cuota(id):
    #modifica el estado de la cuota de NO pagada a SI pagada
    cuota = Cuota.query.get(id)
    cuota.estado_pago = True
    cuota.pagado_en = datetime.now()
    db.session.commit()
    return cuota


def get_idsocio_sincuotaactual(year, month):
    list_idsocio = []
    for c in Cuota.query.filter(extract('month', Cuota.anomes)==month, extract('year', Cuota.anomes)==year):
        list_idsocio.append(c.socio_id)

    return list_idsocio 
    
def get_cuotas_idsocio(idS):
    return Cuota.query.filter_by(socio_id=idS).order_by(Cuota.anomes.desc())

def get_cuotas_nopagadas_socio(idS):
    return Cuota.query.filter_by(socio_id=idS, estado_pago=False).all()

def get_cuotas_nopagadas():
    return Cuota.query.filter_by(estado_pago=False)

def get_cuota_by(id):
    return Cuota.query.get(id)

def get_json(cuota):
    return {
        "fecha_cuota": f"{cuota.anomes.month}/{cuota.anomes.year}",
        "mes": cuota.anomes.month,
        "monto" : cuota.monto,
        "pagado_en" : cuota.pagado_en,
        "flagAumento": cuota.flagAumento
    }

def get_cuotas():
    return Cuota.query.all()

def get_cuotas_pagadas():
    return Cuota.query.filter_by(estado_pago=True).order_by(Cuota.anomes.desc())