from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    config_db(app)

def config_db(app):
    @app.before_first_request #esto no es la mejor estrategia capaz despues hay que borrarlo es para probar
    def init_database():
        #from src.core.models.User import User
        #from src.core.models.Disciplina import Disciplina
        db.create_all()
        print("CREO TODAS LAS TABLAS(?)")

    @app.teardown_request #es para cerrar la base de datos en cada request
    def close_session(exception=None):
        db.session.remove()

def reset_db():
    print("ELIMINANDO BASE DE DATOS")
    db.drop_all() #elimina la base de datos
    print("CREANDO BASE DE DATOS")
    db.create_all() #crea la base de datos
    ### HACER UN SCRIPT QUE ARME UNA DB PARA TENER TODOS LOS MISMOS DATOS
