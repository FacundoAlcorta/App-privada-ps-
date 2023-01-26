import email
from operator import truediv
from flask import abort
from flask import session
from src.core.methods import personalMethod
# from src.core.methods import permisoMethod

def agregar_usuario(session):
    if (personalMethod.get_rol_nombre(session.get(email)) == "Administrador"):
        ''' agregar usuario '''
    else:
        return abort(401)


def check_permission(id,permission):
    if (permission in [row[0] for row in personalMethod.permission(id)]):
        return True
    return False

 
