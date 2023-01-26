from ast import Import
import json
from flask import Flask, jsonify
from flask import render_template, request
from src.core.methods import socioMethod
from src.core.methods import disciplinaMethod
from src.core.models.disciplina import Disciplina

from src.core import database
from src.web.config import config
#from src.core.methods import userMethod
from src.web.helpers.auth import is_authenticated
from src.web.helpers.auth import inscripto
from src.web.helpers.permisos import check_permission


from src.web.helpers import handlers

#Imports de controladores
from src.web.controllers.personal import personal_blueprint
from src.web.controllers.auth import auth_blueprint
from src.web.controllers.socios import socio_blueprint
from src.web.controllers.disciplinas import disciplina_blueprint
from src.web.controllers.configuracion import config_blueprint
from src.web.controllers.apis import apis_blueprint
from src.core import insertar_info
#from flask_login import LoginManager
from flask_cors import CORS

def create_app(env="development", static_folder="static"):
# def create_app(env="development", static_folder="static"):
    ##

    app = Flask(__name__, static_folder=static_folder)
    app.config.from_object(config[env])
    # cors = CORS(app)#, resources={r"/api/*": {"origins": "*"}})

    #app.config['JWT_ACCESS_CSRF_HEADER_NAME']


    #login_manager = LoginManager(app)
    #login_manager.login_view = "login"

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(personal_blueprint)
    app.register_blueprint(socio_blueprint)
    app.register_blueprint(disciplina_blueprint)
    app.register_blueprint(config_blueprint)
    app.register_blueprint(apis_blueprint)

    app.register_error_handler(401,handlers.unauthorized_error)
    app.register_error_handler(404,handlers.not_found_error)
    app.register_error_handler(403,handlers.permission_error)
    
    # database.reset_db()
    database.init_app(app)
    
    app.jinja_env.globals.update(is_authenticated=is_authenticated)
    app.jinja_env.globals.update(check_permission=check_permission)
    app.jinja_env.globals.update(inscripto=inscripto)

     
    # with app.app_context():
    #    insertar_info.insertar()

   
    # Define home
    @app.route("/")
    def home():
        contenido = "Argentina"
        return render_template("home.html")


    
    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()
    
    #@login_manager.user_loader
    # def load_user(user_id):
    #    return userMethod.get_by_id(user_id)
    
    

    return app

