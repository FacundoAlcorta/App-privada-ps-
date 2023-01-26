from xml.dom import INVALID_MODIFICATION_ERR
from src.core.models.rol import Rol
from src.core.models.permisos import Permiso
from src.core.database import db
from sqlalchemy import insert


### CONSULTAR: si cargamos los atr del padre los carga acá?? O tenemos que hacer el __init__ en ambos
def create_permiso(nombre):
    permiso = Permiso(nombre)
    db.session.add(permiso)
    db.session.commit()

def list_permisos():
    return Permiso.query.all()

def get_nombre_by_id(id_permiso):
    return db.session.query.filter_by(id=id_permiso).firts

