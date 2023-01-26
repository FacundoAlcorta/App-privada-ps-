from src.core.methods.rolMethod import get_rol_by_id
from src.core.database import db
from src.core.models.personal import Personal
from src.core.models.permisos import Permiso
from src.core.models.rol import Rol
from src.core.methods import rolMethod
from werkzeug.security import check_password_hash

def list_personal():
    #retorna todo el personal no eliminado lógicamente
    return Personal.query.filter_by(eliminado=False).order_by(Personal.id.desc())

def create_personal(nombre,apellido,email,password,rol_id):
    #genera personal
    user = Personal(nombre,apellido,email,password,rol_id)
    db.session.add(user)
    db.session.commit()

def delete_personal(id):
    #elimina lógicamente Personal (id=#)
    personal = Personal.query.get(id)
    personal.eliminado = True
    db.session.commit()
    return True

def modificar_personal(id, nombre, apellido, email, rol_id):
    #modifica Personal
    personal = Personal.query.get(id)
    personal.nombre = nombre
    personal.apellido = apellido
    personal.email = email
    personal.rol_id = rol_id
    db.session.commit()
    return personal

def change_state(id):
    #cambia el estado bloqueado
    personal = Personal.query.get(id)
    personal.bloqueado = not personal.bloqueado
    db.session.commit()
    return True

def find_personal_by_mail_and_pass(email,password):
    return Personal.query.filter_by(email=email,password=password,bloqueado=False,eliminado=False).first()

def get_by_email(email): ###    REVISAR QUE ESTÉ BLOQUEADO
    #obtenemos Personal por email
    return Personal.query.filter_by(email=email, eliminado=False, bloqueado=False).first()

def get_by_id(id):
    #obtenemos Personal por id
    return Personal.query.filter_by(id=id,eliminado=False).first()

def check_password(self, password):
    #consulta si la password está bien
    return self.password == password
    #check_password_hash(self.password, password)

def asignar_rol(id_personal, rol_id):
    #se asigna Rol al Personal
    rol = rolMethod.get_rol_by_id(rol_id)
    personal = get_by_id(id_personal)
    personal.rol_id = rol.id
    db.session.commit()


def get_rol_nombre(email):
    per = Personal.query.filter_by(email=email).first()
    if (per.rol_id.Nombre == "Administrador"):
        return "Administrador"
    else: 
        return "Personal"
    ### CONSULTAR
    ###return get_rol_by_id(per.rol_id)

def permission(id):
    #obtener Permisos del Rol del Personal.id=id
    user_id = str(id)
    sql_query = 'SELECT p.name FROM personal pl ' \
                    'INNER JOIN roles_permisos r ON r.rol_id = pl.rol_id ' \
				    'INNER JOIN permisos p on r.permiso_id = p.id ' \
					'WHERE pl.id = {} '.format(user_id)
    permisos = db.engine.execute(sql_query)
    return permisos


def personal_bloqueados():
    #retorna Personal bloqueado
    return Personal.query.filter_by(bloqueado=True, eliminado=False).order_by(Personal.id.desc())
    #db.session.filter_by(estado=True).list()

def personal_desbloqueados():
    #retorna Personal no bloqueado
    return Personal.query.filter_by(bloqueado=False, eliminado=False).order_by(Personal.id.desc())

def list_by_email(nombre):
    #retorna Personal que contenga nombre LIKE nombre
    return Personal.query.filter(Personal.email.ilike(f'%{nombre}%')).filter_by(eliminado=False).order_by(Personal.nombre)