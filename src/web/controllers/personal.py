import imp
from flask import Blueprint
from flask import render_template, request, url_for, redirect
from werkzeug.urls import url_parse
#from src.core.models.personal import Personal
from src.core.methods import personalMethod
from src.core.methods import configuracionMethod
from src.web.helpers.auth import login_required, hash_pass
#from src.web.helpers.permisos import permisos_personal
from src.web.forms import SignupForm
from src.web.forms import AgregarPersonalForm, ModificarPersonalForm
from src.web.helpers.permisos import check_permission
from flask import session, abort


personal_blueprint = Blueprint("personal", __name__ , url_prefix="/personal")

@personal_blueprint.get("/")
@login_required
def index():
    if (not check_permission(session["user_id"],permission="personal_index")):
        abort(403)
    #index Personal
    per_page = configuracionMethod.get_paginado()
    page = int(request.args.get('page', 1))
    personal_pagination= personalMethod.list_personal().paginate(page=page,per_page=per_page)
    personal = personalMethod.list_personal()
    url='personal.index'
    return render_template("personal/personal.html",personal=personal, personal_pagination=personal_pagination,url=url)


### CONSULTAR TODOS LOS CASOS
@personal_blueprint.route("/signup", methods=["GET", "POST"])
@login_required
def signup_personal():
    if (not check_permission(session["user_id"],permission="personal_new")):
        abort(403)
    #generar Personal
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        nombre = form.nombre.data
        apellido = form.apellido.data
            # pruebo que no hay ya un usuario con ese email
        personal = personalMethod.get_by_email(email)
        if personal is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
                # creo el usuario y lo guardo
            passw = hash_pass(password)
            personalMethod.create_personal(nombre=nombre, apellido=apellido, email=email, password=passw)
                # set_password(user, password=password)
                # dejo al usuario logueado
                #login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('personas.personas_index')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)

@personal_blueprint.get("/block/<int:id>")
#@login_required
def block_personal(id):
    if (not check_permission(session["user_id"],permission="personal_update")):
        abort(403)
    #cambia estado bloqueado
    personalMethod.change_state(id)
    return redirect("/personal")

@personal_blueprint.get("/delete/<int:id>")
#@login_required
def delete_personal(id):
    if (not check_permission(session["user_id"],permission="personal_destroy")):
        abort(403)
    #elimina lógicamente
    personalMethod.delete_personal(id)
    return redirect("/personal")

### CONSULTAR TODOS LOS CASOS
@personal_blueprint.route("/agregar",  methods=["GET", "POST"])
#@login_required
def agregar_personal():
    if (not check_permission(session["user_id"],permission="personal_new")):
        abort(403)
    #formulario de alta 
    form = AgregarPersonalForm()
    error = None
    if form.validate_on_submit():

        personal = personalMethod.get_by_email(form.email.data)
        if personal is not None:
            error = f'El email ya está siendo utilizado por otro usuario'
        else:
            nombre      = form.nombre.data
            apellido    = form.apellido.data
            email       = form.email.data
            password    = form.password.data
            rol_id      = form.rol_id.data
            submit      = form.submit.data
            personalMethod.create_personal(nombre=nombre, apellido=apellido, email=email, password=password, rol_id=rol_id)
            return redirect("/personal")

    return render_template('personal/agregar_personal_form.html', form=form, error=error)

@personal_blueprint.route("/personal<int:id>", methods=["GET", "POST"])
#@login_required
def show_complete(id):
    if (not check_permission(session["user_id"],permission="personal_show")):
        abort(403)
    #muestra la info personal del Personal
    personal = personalMethod.get_by_id(id=id) 
    return render_template("personal/personal_card.html", personal=personal)


### CONSULTAR TODOS LOS CASOS
@personal_blueprint.route("/modificar<int:id>",  methods=["GET", "POST"])
#@login_required
def modificar_personal(id):
    if (not check_permission(session["user_id"],permission="personal_update")):
        abort(403)
    #modifica Personal
    form = ModificarPersonalForm()
    error = None
    per = personalMethod.get_by_id(id)
    if form.validate_on_submit():
        personal = personalMethod.get_by_email(form.email.data)
        if personal is not None:
            error = f'El email ya está siendo utilizado por otro usuario'
        else:
            nombre      = form.nombre.data
            apellido    = form.apellido.data
            email       = form.email.data
            rol_id      = form.rol_id.data
            submit      = form.submit.data
            personalMethod.modificar_personal(id=id, nombre=nombre, apellido=apellido, email=email, rol_id=rol_id)
            return redirect("/personal")
    return render_template('personal/modificar_personal.html', form=form, error=error, per=per)


@personal_blueprint.route("/bloqueados", methods=['GET'])
def bloqueados():
    if (not check_permission(session["user_id"],permission="personal_index")):
        abort(403)
    #muestra Personal bloqueados
    per_page = configuracionMethod.get_paginado()
    page = int(request.args.get('page', 1))
    personal_pagination= personalMethod.personal_bloqueados().paginate(page=page,per_page=per_page)
    personal = personalMethod.personal_bloqueados()
    url='personal.bloqueados'
    return render_template("personal/personal.html",personal=personal, personal_pagination=personal_pagination,url=url)


@personal_blueprint.route("/desbloqueados", methods=['GET'])
def desbloqueados():
    if (not check_permission(session["user_id"],permission="personal_index")):
        abort(403)
    #muestra Personal Desbloquados
    per_page = configuracionMethod.get_paginado()
    page = int(request.args.get('page', 1))
    personal_pagination= personalMethod.personal_desbloqueados().paginate(page=page,per_page=per_page)
    personal = personalMethod.personal_desbloqueados()
    url='personal.desbloqueados'
    return render_template("personal/personal.html",personal=personal, personal_pagination=personal_pagination,url=url)

@personal_blueprint.route("/email", methods=['GET','POST'])
@login_required
def buscar_email():
    if (not check_permission(session["user_id"],permission="personal_index")):
        abort(403)
    #En el caso de ser la primera vez(la busqueda) , recibe el parametro por POST
    #Para pasar de pagina lo recibe por le metodo GET
    try:
        params = request.form
        nombre = params['nombre']
    except:
        nombre = str(request.args.get('nombre'))
    per_page = configuracionMethod.get_paginado()
    page = int(request.args.get('page', 1))
    personal = personalMethod.list_by_email(nombre)
    personal_pagination = personalMethod.list_by_email(nombre).paginate(page=page,per_page=per_page)
    url = "personal.buscar_email"
    return render_template("personal/personal.html", personal=personal, personal_pagination=personal_pagination,url=url,nombre=nombre)
    