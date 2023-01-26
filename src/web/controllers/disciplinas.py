from unicodedata import category
from flask import Blueprint
from flask import render_template, redirect
#from src.core.models.personal import Personal
from src.core.methods import disciplinaMethod
from src.core.methods import configuracionMethod
#from src.web.helpers.auth import login_required
from src.web.forms import AgregarDisciplinaForm
from src.web.forms import ModificarDisciplinaForm 
from src.web.helpers.permisos import check_permission
from src.web.helpers.auth import login_required
from flask import session, request
from flask import abort


disciplina_blueprint = Blueprint("disciplinas", __name__ , url_prefix="/disciplinas")

@disciplina_blueprint.get("/")
@login_required
def index():
    if (not check_permission(session["user_id"],permission="disciplina_index")):
        abort(403)
    per_page = configuracionMethod.get_paginado()
    page = int(request.args.get('page', 1))
    disciplina_pagination = disciplinaMethod.list_disciplinas().paginate (page=page,per_page=per_page)
    disciplinas = disciplinaMethod.list_disciplinas()
    url = 'disciplinas.index'
    return render_template("disciplinas/disciplinas.html" , disciplinas=disciplinas, disciplina_pagination=disciplina_pagination, url=url)

@disciplina_blueprint.get("/block/<int:id>")
@login_required
def block_discipline(id):
    if not check_permission(session["user_id"],permission="disciplina_update"):
        abort(403)
    disciplinaMethod.change_state(id)
    return redirect("/disciplinas")

@disciplina_blueprint.get("/delete/<int:id>")
@login_required
def delete_disciplina(id):
    if not check_permission(session["user_id"],permission="disciplina_destroy"):
        abort(403)
    disciplinaMethod.delete(id)
    return redirect("/disciplinas")

@disciplina_blueprint.route("/agregar",  methods=["GET", "POST"])
@login_required
def agregar_diciplina():
    #El if es para verificar si el usuario actual de la session tiene los permisos
    #para poder agregar una disciplina, en caso contrario muestra error 403
    if not check_permission(session["user_id"],permission="disciplina_new"):
        abort(403)
    form = AgregarDisciplinaForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        categoria = form.categoria.data
        instructores = form.instructores.data
        dias = form.dias.data
        horarios = form.horario.data
        costo = form.costo_mensual.data
        # habilitada = form.habilitada.data
        disciplinaMethod.create_disciplina(nombre=nombre, categoria=categoria, dias=dias, horario=horarios, costo_mensual=costo, instructores=instructores)
        return redirect("/disciplinas")
    return render_template('disciplinas/agregar_disciplina_form.html', form=form)

@disciplina_blueprint.route("/disciplina<int:id>", methods=["GET", "POST"])
#@login_required
def show_complete(id):
    if not check_permission(session["user_id"],permission="disciplina_index"):
        abort(403)
    disciplina = disciplinaMethod.get_by_id(id=id) 
    return render_template("disciplinas/disciplina_card.html", disciplina=disciplina)

@disciplina_blueprint.route("/modificar/<int:id>",  methods=["GET", "POST"])
@login_required
def modificar_disciplina(id):
    if not check_permission(session["user_id"],permission="disciplina_update"):
        abort(403)
    #modifica disciplina
    disciplina = disciplinaMethod.get_by_id(id)
    form = ModificarDisciplinaForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        categoria = form.categoria.data
        instructores = form.instructores.data
        dias = form.dias.data
        horario = form.horario.data
        costo = form.costo_mensual.data
        print(costo)
        disciplinaMethod.modificar_disciplina(id=id,nombre=nombre, categoria=categoria, dias=dias, horario=horario, costo_mensual=costo,instructores=instructores)
        #return render_template("disciplinas/disciplinas.html", form=form, disciplina=disciplina)
        return redirect("/disciplinas")

    return render_template("disciplinas/modificar_disciplina.html", form=form, disciplina=disciplina)


@disciplina_blueprint.get("/block/<int:id>")
@login_required
def change_state(id):
    if not check_permission(session["user_id"],permission="disciplina_update"):
        abort(403)
    disciplinaMethod.change_state(id)
    return redirect("/disciplinas")


@disciplina_blueprint.route("/deshabilitadas")
@login_required
def deshabilitadas():
    if (not check_permission(session["user_id"],permission="disciplina_index")):
        abort(403)
    per_page = configuracionMethod.get_paginado()
    page = int(request.args.get('page', 1))
    disciplina_pagination = disciplinaMethod.disciplinas_deshabilitadas().paginate (page=page,per_page=per_page)
    disciplinas = disciplinaMethod.disciplinas_deshabilitadas
    url = 'disciplinas.deshabilitadas'
    return render_template("disciplinas/disciplinas.html" , disciplinas=disciplinas, disciplina_pagination=disciplina_pagination, url=url)

@disciplina_blueprint.route("/habilitadas")
@login_required
def habilitadas():
    if (not check_permission(session["user_id"],permission="disciplina_index")):
        abort(403)
    per_page = configuracionMethod.get_paginado()
    page = int(request.args.get('page', 1))
    disciplina_pagination = disciplinaMethod.disciplinas_habilitadas().paginate (page=page,per_page=per_page)
    disciplinas = disciplinaMethod.disciplinas_habilitadas
    url = 'disciplinas.habilitadas'
    return render_template("disciplinas/disciplinas.html" , disciplinas=disciplinas, disciplina_pagination=disciplina_pagination, url=url)