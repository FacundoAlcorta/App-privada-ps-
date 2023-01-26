#from crypt import methods
# from this import d
from flask import Blueprint
from flask import render_template, redirect
from src.core.methods import disciplinaMethod
#from src.core.models.personal import Personal
from src.core.methods import socioMethod
from src.core.methods import cuotaMethod
from src.core.methods import configuracionMethod
from src.web.helpers.auth import login_required
from src.web.forms import AgregarSocioForm, ModificarSocioForm
from src.web.helpers.permisos import check_permission
from src.web.helpers.auth import hash_pass
from flask import session
from flask import request, send_file
from flask import abort
import qrcode
from PIL import Image, ImageDraw
from fpdf import FPDF
from urlextract import URLExtract
import csv
from pathlib import Path, PurePath
from flask_jwt_extended import set_access_cookies, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies




socio_blueprint = Blueprint("socios", __name__ , url_prefix="/socios")

@socio_blueprint.get("/")
@login_required
def index():
    if not check_permission(session["user_id"],permission="socio_index"):
        abort(403)
    per_page = configuracionMethod.get_paginado()
    page = int(request.args.get('page', 1))
    socio_pagination = socioMethod.list_socios().paginate(page=page,per_page=per_page)
    #socio_pagination = socioMethod.list_paginados(page,per_pag)
    socios = socioMethod.list_socios()
    url = 'socios.index'
    return render_template("socios/socio2.html", socios=socios, socio_pagination=socio_pagination,url=url)

@socio_blueprint.get("/block/<int:id>")
@login_required
def block_socio(id):
    if not check_permission(session["user_id"],permission="socio_update"):
        abort(403)
    socioMethod.change_state(id)
    return redirect("/socios")

@socio_blueprint.get("/delete/<int:id>")
@login_required
def delete_socio(id):
    if not check_permission(session["user_id"],permission="socio_update"):
        abort(403)
    socioMethod.delete_socio(id)
    return redirect("/socios")

@socio_blueprint.route("/agregar",methods=["GET", "POST"])
@login_required
def agregar_socio():
    if not check_permission(session["user_id"],permission="socio_new"):
        abort(403)
    form = AgregarSocioForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        apellido = form.apellido.data
        tipo_documento = form.tipo_documento.data
        documento = form.documento.data
        genero = form.genero.data
        direccion = form.direccion.data
        telefono = form.telefono.data
        email = form.email.data
        password = hash_pass('1234')
        submit = form.submit.data
        socioMethod.create_socio(nombre=nombre, apellido=apellido, password=password, tipo_documento=tipo_documento, documento=documento, genero=genero, direccion=direccion, telefono=telefono,email=email)
        return redirect("/socios")

    return render_template('socios/agregar_socio_form.html', form=form)\

@socio_blueprint.route("/socio<int:id>", methods=["GET", "POST"])
@login_required
def show_complete(id):
    if not check_permission(session["user_id"],permission="socio_index"):
        abort(403)
    socio = socioMethod.get_socios_by_id(id=id) 
    cuotas = cuotaMethod.get_cuotas_idsocio(idS=id)

    return render_template("socios/socio_card.html", socio=socio, cuotas=cuotas)


# @socio_blueprint.route("/socio<int:id>/imprimir", methods=["GET", "POST"])
# def imprimir_socio(id):
#     pdfkit.from_file("/home/usuario/grupo09/admin/src/web/templates/socios/socio_card.html", "generar.pdf", verbose=True, options={"enable-local-file-access": True})
#     return show_complete(id)


@socio_blueprint.route("/modificar/<int:id>",methods=["GET", "POST"])
@login_required
def modificar_socio(id):
    if not check_permission(session["user_id"],permission="socio_update"):
        abort(403)
    print(id)
    socio = socioMethod.get_socios_by_id(id)
    form = ModificarSocioForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        apellido = form.apellido.data
        tipo_documento = form.tipo_documento.data
        documento = form.documento.data
        genero = form.genero.data
        direccion = form.direccion.data
        telefono = form.telefono.data
        email = form.email.data
        submit = form.submit.data
        socioMethod.modificar_socio(id=id, nombre=nombre, apellido=apellido, tipo_documento=tipo_documento, documento=documento, genero=genero, direccion=direccion, telefono=telefono,email=email)
        return redirect("/socios")

    return render_template('socios/modificar_socio.html', form=form, socio=socio)

@socio_blueprint.route("/bloqueados")
@login_required
def bloqueados():
    if not check_permission(session["user_id"],permission="socio_index"):
        abort(403)
    per_page = configuracionMethod.get_paginado()
    page = int(request.args.get('page', 1))
    socio_pagination =  socioMethod.socios_bloqueados().paginate(page=page, per_page=per_page)
    socios = socioMethod.socios_desbloqueados()
    url = 'socios.bloqueados'
    return render_template("socios/socio2.html",  socios=socios , socio_pagination=socio_pagination,url=url)

def download_csv():
    return send_file("/home/grupo09/app/current/admin/public/socios.csv", as_attachment=True)
def download_pdf():
    return send_file("/home/grupo09/app/current/admin/public/socios.pdf", as_attachment=True)

@socio_blueprint.get("/pdf")
def generar_pdf():
    downloads_path = str(Path.home()) + "/socio.pdf"

    aux = request.args.get("url")
    #socios = socioMethod.generar_lista_csv(aux)
    socios = None
    print(aux)
    if(aux == 'socios.index'):
        socios = socioMethod.list_socios()
    elif(aux == 'socios.bloqueados'):
        socios = socioMethod.socios_bloqueados()
    elif(aux == 'socios.desbloqueados'):
        socios = socioMethod.socios_desbloqueados()
    elif(aux == 'socios.buscar_apellido'):
        socios = socioMethod.list_by_apellido(request.args.getlist("apellido"))
    if not socios:
    #aca no se genera si esta vacio falta cartel que avise que no se genero por estar vacio
        print("vaciia")
    else:
        # save FPDF() class into a
        # variable pdf
        pdf = FPDF()
            
            # Add a page
        pdf.add_page()
            
            # set style and size of font
            # that you want in the pdf
        pdf.set_font("Arial", size = 15)
            
            # create a cell
        pdf.cell(200, 10, txt = "Socios",
                    ln = 1, align = 'C')
            
            # add another cell
        pdf.cell(200, 10, txt = "Información de socios.",
                ln = 2, align = 'C')

        pdf.cell(200, 5, txt = 'Nombre, Apellido, Tipo, Documento, Genero, Dirección, Tel, email',
                ln = 2, align = 'C')
        for socio in socios:
            pdf.cell(200, 5, txt = socio.nombre +' | '+ socio.apellido +' | '+ socio.tipo_documento +' | '+ str(socio.documento) +' | '+ socio.genero +' | '+ socio.direccion +' | '+ str(socio.telefono) +' | '+ socio.email,
                ln = 2, align = 'C')
            
            # save the pdf with name .pdf
        #pdf.output('/home/grupo09/app/current/admin/public/socios.pdf')  
        pdf.output(downloads_path)

        #return send_file("/home/grupo09/app/current/admin/public/socios.pdf", as_attachment=True)
        return send_file(downloads_path, as_attachment=True)




@socio_blueprint.get("/csv")
def generar_csv():

    downloads_path = str(Path.home())
    out_path = downloads_path + "socios.csv"

    aux = request.args.get("url")
    #socios = socioMethod.generar_lista_csv(aux)
    socios = None
    print(aux)
    if(aux == 'socios.index'):
        socios = socioMethod.list_socios()
    elif(aux == 'socios.bloqueados'):
        socios = socioMethod.socios_bloqueados()
    elif(aux == 'socios.desbloqueados'):
        socios = socioMethod.socios_desbloqueados()
    elif(aux == 'socios.buscar_apellido'):
        socios = socioMethod.list_by_apellido(request.args.getlist("apellido"))
    if not socios:
    #aca no se genera si esta vacio falta cartel que avise que no se genero por estar vacio
        print("vaciia")
    else:
        origin_path = downloads_path + "/socios.csv"

        #with open('/home/grupo09/app/current/admin/public/socios.csv', 'w', newline='') as nuevocsv:
        with open(origin_path, 'w', newline='') as nuevocsv:
            writer = csv.writer(nuevocsv)
            writer.writerow(["NOMBRE","APELLIDO","TIPO DOC","DOCUMENTO","GENERO","DIRECCION","TELEFONO","EMAIL"])
            for socio in socios:
                writer.writerow([socio.nombre, socio.apellido, socio.tipo_documento, socio.documento, socio.genero, socio.direccion, socio.telefono, socio.email])

        origin_path = downloads_path + "/socios.csv"
        
        return send_file(origin_path, as_attachment=True);

        # return send_file("/home/grupo09/app/current/admin/public/socios.csv", as_attachment=True)

    return redirect("/socios")



@socio_blueprint.route("/desbloqueados")
@login_required
def desbloqueados():
    if not check_permission(session["user_id"],permission="socio_index"):
        abort(403)
    per_page = configuracionMethod.get_paginado()
    page = int(request.args.get('page', 1))
    socio_pagination =  socioMethod.socios_desbloqueados().paginate(page=page, per_page=per_page)
    socios = socioMethod.socios_desbloqueados()
    url = 'socios.desbloqueados'
    return render_template("socios/socio2.html", socios=socios, socio_pagination=socio_pagination, url=url)

@socio_blueprint.route("/apellido", methods=['GET','POST'])
@login_required
def buscar_apellido():
    if not check_permission(session["user_id"],permission="socio_index"):
        abort(403)
    try:
        params = request.form
        apellido = params['apellido']
    except:
        apellido = str(request.args.get('apellido'))
    per_page = configuracionMethod.get_paginado()
    page = int(request.args.get('page', 1))
    socios = socioMethod.list_by_apellido(apellido)  
    socio_pagination =  socioMethod.list_by_apellido(apellido).paginate(page=page, per_page=per_page)
    url = "socios.buscar_apellido"
    return render_template("socios/socio2.html",  socios=socios, socio_pagination=socio_pagination, url=url, apellido=apellido )

@socio_blueprint.route("/inscripcion/<int:id>",methods=["GET", "POST"])
@login_required
def inscripcion_disciplina(id):
    if not check_permission(session["user_id"],permission="socio_update"):
        abort(403)
    disciplinas = disciplinaMethod.disciplinas_habilitadas()
    return render_template('socios/inscripcion_disciplina.html',id_socio=id, disciplinas=disciplinas)

@socio_blueprint.route("/bajaDisciplina/<int:id_disc>/<int:id_soc>")
@login_required
def baja_disciplina(id_disc,id_soc):
    if not check_permission(session["user_id"],permission="socio_update"):
        abort(403)
    #socioMethod.delete_socio(id)
    #Por el momento no
    socioMethod.baja_disciplina(id_soc,id_disc)
    return redirect(f"/socios/inscripcion/{ id_soc }")

@socio_blueprint.route("/altaDisciplina/<int:id_disc>/<int:id_soc>")
@login_required
def alta_disciplina(id_disc,id_soc):
    if not check_permission(session["user_id"],permission="socio_update"):
        abort(403)
    #socioMethod.delete_socio(id)
    #Por el momento no
    socioMethod.agregar_disciplina(id_soc,id_disc)
    print("DISCIPLINA AGREGADA")
    return redirect(f"/socios/inscripcion/{ id_soc }")


@socio_blueprint.route("/socio<int:id>/imprimir", methods=["GET", "POST"])
@login_required
def imprimir_socio(id):
    downloads_path = str(Path.home()) + "/card.pdf"
    socio = socioMethod.get_socios_by_id(id=id)
    # save FPDF() class into a
        # variable pdf
    if (socio.moroso):
        rta = "Con deuda pendiente."
    else:
        rta = "Pagos al día."
    pdf = FPDF()
            
            # Add a page
    pdf.add_page()
            
            # set style and size of font
            # that you want in the pdf
    pdf.set_font("Arial", size = 15)
            
            # add another cell
    pdf.cell(200, 16, txt = "Clun Deportivo Villa Elisa.",
                ln = 1, align = 'C')
    pdf.cell(200, 10, txt = "Nombre: " + str(socio.nombre),
                ln = 2, align = 'L')
    pdf.cell(200, 10, txt = "Apellido: " + str(socio.apellido),
                ln = 3, align = 'L')
    pdf.cell(200, 10, txt = "Documento: " + str(socio.documento),
                ln = 4, align = 'L')
    pdf.cell(200, 10, txt = "Fecha alta: : " + str(socio.fecha_inicio.strftime('%Y-%m-%d')),
                ln = 5, align = 'L')
    pdf.cell(200, 10, txt = "Estado: " + rta,
                ln = 6, align = 'L')


    qr = qrcode.QRCode(
    version = 1,
    error_correction = qrcode.constants.ERROR_CORRECT_H,
    box_size = 10,
    border = 4
                        )
# Podemos crear la informacion que queremos 
# en el codigo de manera separada
    
    
    #urls = url_for(show_complete(id))
    #print(urls)
    
    info = f"https://admin-grupo09.proyecto2022.linti.unlp.edu.ar/socios/socio{id}"
    qr.add_data(info)
    qr.make(fit=True)
    imagen = qr.make_image()
    imagen.save('codigo.png')

    pdf.image('codigo.png', 150, 15, 50)

    pdf.output(downloads_path)

    #pdfkit.from_file("/home/usuario/grupo09/admin/src/web/templates/socios/socio_card.html", "generar.pdf", verbose=True, options={"enable-local-file-access": True})
    return send_file(downloads_path, as_attachment=True)


