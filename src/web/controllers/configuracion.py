from contextlib import nullcontext
from flask import Blueprint
from flask import render_template, redirect
from src.core.methods import cuotaMethod
from src.core.methods import socioMethod
from src.core.methods import disciplinaMethod
from src.core.methods import configuracionMethod

from src.web.helpers.permisos import check_permission
from src.web.helpers.auth import login_required
from flask import session
from flask import abort

from datetime import date
from datetime import datetime
from flask import request




config_blueprint = Blueprint("config", __name__ , url_prefix="/config")

@config_blueprint.route("/config", methods=['GET','POST'])
@login_required
def actualizar_paginado():
    if not check_permission(session["user_id"],permission="socio_index"):
        abort(403)
    print(configuracionMethod.get_monto_base)

    params = request.form
    nuevo_paginado = params['paginado']
    if(nuevo_paginado in('5','10','15','20')):
        configuracionMethod.modificar_paginado(paginado=int(nuevo_paginado))

    monto_base = params['monto_base']
    if(monto_base.isnumeric() and int(monto_base)>0):
        configuracionMethod.modificar_monto_base(monto_base)

    porcentaje = params['porcentaje']
    if(nuevo_paginado in('5','10','15','20')):
        configuracionMethod.modificar_porcentaje(porcentaje)


    return redirect("/config")





@config_blueprint.get("/")
def index():
    if not check_permission(session["user_id"],permission="config_show"):
        abort(403)
    # if (not check_permission(session["user_id"],permission="disciplina_index")):
    #     print("no tiene permiso")
    #     abort(401)
    return render_template("config/config.html" )

### CREAR CUOTAS
@config_blueprint.get("/new")
#@login_required
def generar_cuotas():
    if not check_permission(session["user_id"],permission="cuota_generate"):     ###CONSULTA
         abort(403)    
    ### traer id de todos los socios no bloqueados
    socios_list = socioMethod.get_socios_id()
    print('SOCIOS ACTUALES:', socios_list )
   
    ###obtener id socios desde cuotas del mes no creadas
    ## año y mes actual
    actual_year= str(datetime.today().year)
    actual_month= str(datetime.today().month)
    list_idsocio_sin_cuotas = cuotaMethod.get_idsocio_sincuotaactual(actual_year, actual_month)
    print('SOCIOS CON CUOTAS DEL MES:',list_idsocio_sin_cuotas)

    list_idsocios_sincuota = list(set(socios_list) - set(list_idsocio_sin_cuotas))
    print('CREAR CUOTAS A SOCIOS:',list_idsocio_sin_cuotas)

    ### obtener dict de id_disciplina:monto
    disciplinas_monto = disciplinaMethod.get_montos()
    print(disciplinas_monto)

    ### obtener monto base de la configuracion
    monto_base = configuracionMethod.get_configuration().monto_base
    print('MONTO BASE', monto_base)

    for idsocio in list_idsocios_sincuota:
        monto = monto_base
        disciplinas_socio = socioMethod.disciplina_practicada(idsocio)
        for iddisciplina in disciplinas_socio:
            print(iddisciplina.id)
            print(iddisciplina.id)
            print(iddisciplina.id)
            print(iddisciplina.id)
            print(iddisciplina.id)
            monto += disciplinas_monto[iddisciplina.id]
        print(monto)
        cuotaMethod.create_cuota(monto, idsocio)

    return redirect("/config")


###DEJA DE SER MOROS?
def sigue_moroso(socio, cuotas):
    ### calcular si deja ser moroso
    if(socio.moroso):
        actual_year= str(datetime.today().year)
        actual_month= str(datetime.today().month)
        es_moroso = False
        for cuota in cuotas:
            if(actual_year == str(cuota.anomes.year) and actual_month == str(cuota.anomes.month) and (cuota.anomes.day <= 10)):
            # si es la cuota actual y estamos antes del 10 no se calcula
                next
            if(not cuota.estado_pago):
            # si la cuota NO está pagada SIGUE MOROSO
                es_moroso = True
                break
        print(es_moroso)
                
        if(not es_moroso):
            # deja de ser MOROSO
            socioMethod.change_moroso(socio.id, False)


### PAGAR CUOTA
@config_blueprint.get("/pagar/<int:idC>/<int:idS>")
@login_required
def pagar_cuotas(idC, idS):
    #pagar una cuota
    #if not check_permission(session["user_id"],permission="pagos_show"):     ###CONSULTA
    #   abort(403)

    cuotaMethod.pago_cuota(idC) 
    socio = socioMethod.get_socios_by_id(id=idS)
    cuotas = cuotaMethod.get_cuotas_idsocio(idS=idS)

    sigue_moroso(socio, cuotas)

    return render_template("socios/socio_card.html", socio=socio, cuotas=cuotas)        

### CALCULAR MOROSOS E INCREMENTAR CUOTAS
@config_blueprint.get("/edit")
#@login_required
def calcular_cuotas():
    if not check_permission(session["user_id"],permission="config_update"):     ###CONSULTA
        abort(403)

    actual_year= str(datetime.today().year)
    actual_month= str(datetime.today().month)
    
    # traer todas las cuotas no pagadas
    cuotas_nopagadas = cuotaMethod.get_cuotas_nopagadas()

    # porcentaje de recargo de la configuracion
    porcentaje_recargo = configuracionMethod.get_configuration().porcentaje_recargo

    # listado de socios que pasan a ser morosos
    list_sociosid = []

    for cuota in cuotas_nopagadas:
        if(actual_year == str(cuota.anomes.year) and actual_month == str(cuota.anomes.month) and (cuota.anomes.day <= 10)):
            # si es la cuota actual y estamos antes del 10 no se calcula
            next
        if not cuota.flagAumento:
            nuevo_monto = cuota.monto + cuota.monto * porcentaje_recargo / 100
            cuotaMethod.aumento_por_atraso(cuota.id, nuevo_monto)
            list_sociosid.append(cuota.socio_id)
            
    list_sociosid = list(set(list_sociosid))
    for socioid in list_sociosid:
        # deja a los socios en estado MOROSO
        print(socioid)
        socioMethod.change_moroso(socioid, True)






    return render_template("config/config.html" )

### EXPORTAR PDF

@config_blueprint.route("/exportarCuota/<int:idC>/<int:idS>")
@login_required
def exportar_cuota(idC, idS):
    import csv
    from fpdf import FPDF
    import os 
    from flask import send_file


    # aux = request.args.get("idC")
    cuota = cuotaMethod.get_cuota_by(idC)
    socio = socioMethod.get_socios_by_id(idS)
    # encabezado = configuracionMethod.get_encabezado()
        # save FPDF() class into a
        # variable pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)

    pdf.cell(200, 10, txt = "Cuota",ln = 1, align = 'C')
    pdf.cell(200, 10, txt = "Información de cuotas.",ln = 2, align = 'C')
    pdf.cell(200,10,txt= "Recibo # " + str(cuota.id),ln = 2, align = 'C')
    pdf.cell(200,10,txt= "Fecha de emision: " + str(cuota.anomes.year) + " / "+ str(cuota.anomes.month),ln = 2, align = 'C')
    pdf.cell(200,10,txt= "Nombre del socio: " + str(socio.nombre),ln = 2, align = 'C')
    pdf.cell(200,10,txt= "Monto: " + str(cuota.monto),ln = 2, align = 'C')
    pdf.cell(200,10,txt= "Por el concepto de cuota societria mes" + str(cuota.anomes.year) + " / "+ str(cuota.anomes.month),ln = 2, align = 'C')
    
    pdf.output('/home/grupo09/app/current/admin/public/cuota.pdf')
    return send_file("/home/grupo09/app/current/admin/public/cuota.pdf", as_attachment=True)
    return redirect("/home/grupo09/app/current/admin/public/exportarCuota")
