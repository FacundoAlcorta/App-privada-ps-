from functools import wraps
from operator import truediv
from flask import abort
from flask import session
from src.core.methods import socioMethod
from werkzeug.security import generate_password_hash, check_password_hash

def is_authenticated(session):
    return session.get("user")!=None

def hash_pass(pas):
    return generate_password_hash(pas, method='sha256')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return abort(401)
        return f(*args,**kwargs)
    return decorated_function

def inscripto(id_socio, id_disciplina):
    '''
    if (id_disciplina in [row[0] for row in socioMethod.disciplina_practicada(id_socio)]):
        print("------")
        return True
    print("/////////")
    return False
    '''
    if(id_disciplina in [row.id for row in socioMethod.disciplina_practicada(id_socio)]):
        print("------------")
        return True
    return False
