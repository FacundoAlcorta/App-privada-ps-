import imp
from logging.handlers import SocketHandler
from select import select
from xml.dom import INVALID_MODIFICATION_ERR
from src.core.models.disciplina import Disciplina
from src.core.database import db
from src.core.models.socio import Socio, socio_disciplina
from sqlalchemy import insert
from src.core.methods import disciplinaMethod
from src.core.models.cuota import Cuota


    
def list_socios():
    return Socio.query.filter_by(eliminado=False).order_by(Socio.id.desc())

def create_socio(nombre,apellido,password,tipo_documento,documento,genero,direccion,telefono,email):
    user = Socio(nombre,apellido, password,tipo_documento,documento,genero,direccion,telefono,email)
    db.session.add(user)
    db.session.commit()

def delete_socio(id):
    #elimina lógicamente Socio (id=#)
    socio = Socio.query.get(id)
    socio.eliminado = True
    db.session.commit()
    return True

def change_state(id):
    #cambio el estado del Socio (id=#)
    socio = Socio.query.get(id)
    socio.estado = not socio.estado
    db.session.commit()
    return True

def modificar_socio(id, nombre, apellido, tipo_documento, documento, genero, direccion, telefono, email):
    #modifica socio
    socio = Socio.query.get(id)
    socio.nombre = nombre
    socio.apellido = apellido
    #socio.fecha_inicio = fecha_inicio
    socio.tipo_documento = tipo_documento
    socio.documento = documento
    socio.genero = genero
    socio.direccion = direccion
    #socio.estado = estado
    socio.telefono = telefono
    socio.email = email
    db.session.commit()
    return socio

def get_socios_by_id(id):
    #socio con id=id
    return Socio.query.filter_by(id=id, eliminado=False).first()

def agregar_disciplina(id_socio, id_disciplina):
    #agrega disciplina a socio
    #db.session.query(f"INSERT INTO socio_disciplina VALUES {id_socio},{id_disciplina}")
    #stmt = ( insert(socio_disciplina).values(name={id_socio}, fullname={id_disciplina}))
    #db.session.query(insert(socio_disciplina).values(name={id_socio}, fullname={id_disciplina}))
    socio = get_socios_by_id(id_socio)
    #get_socios_by_id(id_socio)
    disc =  Disciplina.query.get(id_disciplina)
    socio.disciplinas.append(disc)
    db.session.commit()

def disciplina_practicada(id_socio):
    #???
    socio = Socio.query.get(id_socio)
    return socio.disciplinas

def socios_bloqueados():
    #get socios bloqueados
    return Socio.query.filter_by(estado=True, eliminado=False).order_by(Socio.id.desc())

def socios_desbloqueados():
    #get socios desbloqueados
    return Socio.query.filter_by(estado=False, eliminado=False).order_by(Socio.id.desc())

def list_by_name(nombre):
    #get socios nombre LIKE nombre
    return Socio.query.filter(Socio.nombre.ilike(f'%{nombre}%'), eliminado=False).order_by(Socio.id.desc())

def list_by_apellido(apellido):
    #get socios nombre LIKE nombre
    return Socio.query.filter(Socio.apellido.ilike(f'%{apellido}%')).filter_by(eliminado=False).order_by(Socio.id.desc())
    
def generar_lista_csv(sociosaux):
    return db.engine.execute(sociosaux[0])


def get_socios_id():
    return [s.id for s in Socio.query.filter_by(eliminado=False, estado=False)]

    '''list_idsocio = []
    for s in Socio.query.filter_by(eliminado=False, estado=False):
        list_idsocio.append[s.id]
    return list_idsocio '''

def get_by_dni(dni):
    return Socio.query.filter_by(documento=dni).first()


# def get_socios_id_mesAct(year_month):
#     from datetime import datetime
#     return Socio.query.filter_by(eliminado=False, fecha_inicio.strftime('%Y %m') = year_month)

# def get_sociosID_from_cuotasNoGeneradas():
#     sql_query =    'SELECT s.id FROM Socios s' \
#                     'WHERE NOT EXISTS (' \
#                     '    SELECT c.socio_id FROM Cuotas c' \
#                     '    WHERE (YEAR(anomes) = YEAR(getDate()) AND (MONTH(anomes) = MONTH(getDate()) )' \
#                     # 'AND s.estado = False AND s.eliminado = False'
#     return  db.engine.execute(sql_query)

def mis_disciplinas(socio_id):
    mis = db.session.query(socio_disciplina).filter_by(socio_id=socio_id).all()
    mis_dis = []
    for d in mis:
        mis_dis.append(disciplinaMethod.get_by_id(d.disciplina_id))
    return mis_dis

def mis_pagos(socio_id):
    return db.session.query(Cuota).filter_by(socio_id=socio_id, estado_pago=True).all()

def cuotas_faltantes(socio_id):
    return db.session.query(Cuota).filter_by(socio_id=socio_id, estado_pago=False).all()

def get_sociosID_from_cuotasNoGeneradas():
    sql_query =    'SELECT s.id FROM Socios s' \
                    'WHERE NOT EXISTS (' \
                    '    SELECT c.socio_id FROM Cuotas c' \
                    '    WHERE (YEAR(anomes) = YEAR(getDate()) AND (MONTH(anomes) = MONTH(getDate()) )' \
                    # 'AND s.estado = False AND s.eliminado = False'
    return  db.engine.execute(sql_query)


def disciplina_practicada(id_socio):
    #???
    socio = get_socios_by_id(id_socio)
    return socio.disciplinas

def baja_disciplina(id_socio,id_disciplina):
    socio= db.session.query(Socio).get(id_socio)
    disciplina= db.session.query(Disciplina).get(id_disciplina)
    socio.disciplinas.remove(disciplina)
    #db.session.query(socios_disciplinas).filter_by(socio_id=id_socio,disciplina_id=id_disciplina).delete
    db.session.commit()
    print("ELIMINANDO RELACION")

def list_paginados(page,per_page):
    return Socio.query.filter_by(eliminado=False).order_by(Socio.nombre.asc()).paginate(page=page, per_page=per_page)

def change_moroso(id, estado_moroso):
    #cambio el estado de morosidad (id=#)
    socio = Socio.query.get(id)
    socio.moroso = estado_moroso
    db.session.commit()
    return True

def get_socios():
    return Socio.query.filter_by(eliminado=False)
