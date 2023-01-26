from flask import Blueprint
from flask import render_template
from src.core.methods import personalMethod, socioMethod
#from src.core.methods import userMethod
from werkzeug.urls import url_parse
from flask import redirect 
from flask import url_for
from flask import request
from flask import session, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from flask_jwt_extended import unset_jwt_cookies, jwt_required
from flask_jwt_extended import get_jwt_identity

auth_blueprint= Blueprint("auth", __name__,url_prefix="/auth")

@auth_blueprint.get("/")
def login():
    return render_template("auth/login.html")
	
@auth_blueprint.post("/authenticate")
def authenticate (): 
    params=request.form
    user = personalMethod.get_by_email(params["email"])
    print(personalMethod.personal_bloqueados())
    if not user:
        return redirect(url_for("auth.login"))
    if check_password_hash(user.password, params["password"]):        ### esto usar despues 
    # if personalMethod.check_password(user.password):
        session["user"] = user.email
        session["nombre"] = user.nombre
        session["user_id"] = user.id
        return redirect(url_for("home"))
    return redirect(url_for("auth.login"))



@auth_blueprint.get("/logout")
def logout():
    del session["user"]
    del session["nombre"]
    del session["user_id"]

    session.clear
    print("aca va mensaje que se cerro sesion")
    return redirect(url_for("auth.login"))

@auth_blueprint.post('/login_jwt')
def login_jwt():
  data = request.get_json()
  dni = data['dni']
  password = data['password']
  user = socioMethod.get_by_dni(dni)
  if user:
    if check_password_hash(user.password, password): #Falta agregarle al modelo contraseña
        access_token = create_access_token(identity=user.id)
        response = jsonify()
        set_access_cookies(response, access_token)
        return response, 201
  return jsonify(message="Unauthorized"), 401

@auth_blueprint.get('/logout_jwt')
@jwt_required( )
def logout_jwt():
  response = jsonify()
  unset_jwt_cookies(response)
  return response, 200

