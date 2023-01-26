from xml.dom import INVALID_MODIFICATION_ERR
from src.core.models.rol import Rol
from src.core.models.permisos import Permiso
from src.core.database import db
from sqlalchemy import insert


### CONSULTAR: si cargamos los atr del padre los carga acá?? O tenemos que hacer el __init__ en ambos
def create_rol(nombre):
    rol = Rol(nombre)
    db.session.add(rol)
    db.session.commit()

def list_roles():
    return Rol.query.all()

def agregar_permiso(id_rol , id_permiso):
    rol = Rol.query.get(id_rol)
    permiso = Permiso.query.get(id_permiso)
    rol.permisos.append(permiso)
    db.session.commit()

def permisos_asignados(id_rol):
    rol = Rol.query.get(id_rol)
    return (rol.permisos)

def get_rol_by_id(id_rol):
    return Rol.query.get(id_rol)




