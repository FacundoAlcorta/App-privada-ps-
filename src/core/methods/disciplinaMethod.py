from src.core.models.disciplina import Disciplina
from src.core.database import db

def create_disciplina(nombre, categoria, dias, horario, costo_mensual, instructores): #para modificar la bdd, con el commit se hacen concretos los cambios
    disciplina = Disciplina(nombre, categoria, dias, horario, costo_mensual, instructores)
    db.session.add(disciplina)
    db.session.commit()
    return disciplina

def delete(id):
    ''' elimina lógicamente Disciplina (id=#) '''
    disciplina = Disciplina.query.get(id)
    disciplina.eliminado = True
    db.session.commit()
    return True

def change_state(id):
    ''' cambio el estado de la disciplina Disciplina (id=#) '''
    disciplina = Disciplina.query.get(id)
    disciplina.estado = not disciplina.estado
    db.session.commit()
    return True


def modificar_disciplina(id, nombre, categoria, dias, horario, costo_mensual, instructores):
    disciplina = Disciplina.query.get(id)
    disciplina.nombre = nombre
    disciplina.categoria = categoria
    disciplina.dias = dias
    disciplina.horario = horario
    disciplina.costo_mensual = costo_mensual
    disciplina.instructores = instructores
    db.session.commit()
    return disciplina

def list_disciplinas():
    return Disciplina.query.filter_by(eliminado=False).order_by(Disciplina.id)

def get_by_id(id):
    #return Disciplina.query.get(id)
    return Disciplina.query.filter_by(id=id, eliminado=False).first()

def list_socios(id_disciplina):
    return Disciplina.query.filter_by(id=id_disciplina)

def get_montos():
    dict_disciplinas = {}
    for d in Disciplina.query.filter_by(eliminado=False, estado=False).order_by(Disciplina.id):
        dict_disciplinas[d.id] = d.costo_mensual

    return dict_disciplinas

def get_json(disciplina):
    return {
        "name" : disciplina.nombre,
        "days" : disciplina.dias,
        "time" : disciplina.horario,
        "teacher" : disciplina.instructores,
        "money": disciplina.costo_mensual
    }

def disciplinas_habilitadas():
    #get socios desbloqueados
    return Disciplina.query.filter_by(estado=False).order_by(Disciplina.id.desc())

def disciplinas_deshabilitadas():
    #get socios desbloqueados
    return Disciplina.query.filter_by(estado=True).order_by(Disciplina.id.desc())
