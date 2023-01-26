from src.core.models.configuracion import Configuracion
from src.core.database import db


def create_configuracion(paginacion, monto_base, porcentaje_recargo):
    configuracion = Configuracion(paginacion, monto_base, porcentaje_recargo)
    db.session.add(configuracion)
    db.session.commit()
    return configuracion

def edit(id, paginacion,orden, monto_base, porcentaje_recargo):
    configuracion = Configuracion.query.get(id)
    configuracion.paginacion = paginacion
    configuracion.orden = orden
    configuracion.monto_base = monto_base
    configuracion.porcentaje_recargo = porcentaje_recargo
    db.session.commit()
    return configuracion

def modificar_paginado(paginado):
    configuracion = Configuracion.query.get(1)
    configuracion.paginacion = paginado
    db.session.commit()
    return configuracion

def get_configuration():
    return Configuracion.query.get(1)

# def get_configuration():
#     ''' retorna todos los valores de la config '''
#     return Configuracion.query.all()

def get_paginado():
    return Configuracion.query.get(1).paginacion
def get_monto_base():
    return Configuracion.query.get(1).first.monto_base

def modificar_monto_base(monto_base):
    configuracion = Configuracion.query.get(1)
    configuracion.monto_base = monto_base
    db.session.commit()
    return configuracion
def modificar_porcentaje(porcentaje):
    configuracion = Configuracion.query.get(1)
    configuracion.porcentaje_recargo = porcentaje
    db.session.commit()
    return configuracion