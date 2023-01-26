from flask import request
from flask import Blueprint
from flask import jsonify
from src.core.methods import disciplinaMethod
from src.core.methods import socioMethod, cuotaMethod
from collections import Counter
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from flask_jwt_extended import unset_jwt_cookies, jwt_required
from flask_jwt_extended import get_jwt_identity



apis_blueprint = Blueprint("apis", __name__ , url_prefix="/api")


@apis_blueprint.route("/club/info", methods=["GET"])
def datos_club():
    datos = [
        {'email': "clubdeportivovillaelisa@gmail.com",
        'phone': "0221 487-0193"}
    ]
    return jsonify(datos)

@apis_blueprint.route("/club/disciplines", methods=["GET"])
def datos_disciplinas():
    disciplinas = disciplinaMethod.list_disciplinas()
    return jsonify(disciplinas_lista=[disciplinaMethod.get_json(i) for i in disciplinas])

@apis_blueprint.route("/me/disciplines", methods=["GET"])
@jwt_required()
def disciplinas_socio():
    id = get_jwt_identity()
    disciplinas = socioMethod.mis_disciplinas(id)
    if disciplinas:
        return jsonify(disciplinas_asociado=[disciplinaMethod.get_json(i) for i in disciplinas])
    else:
        return jsonify("vacio")

#@apis_blueprint.route("/me/payments", methods=["GET"])
@apis_blueprint.route("/<int:id>/payments", methods=["GET"])
#@jwt_required()
def mis_pagos(id):
    # genera API GET de las cuotas pagadas
    #id = get_jwt_identity()
    def get_json(cuota):
        return {
            "fecha_cuota": f"{cuota.anomes.month}/{cuota.anomes.year}",
            "mes": cuota.anomes.month,
            "monto" : cuota.monto,
            "pagado_en" : cuota.pagado_en,
            "flagAumento": cuota.flagAumento
        }
    #cuotas = socioMethod.cuotas_faltantes(id)
    cuotas = cuotaMethod.get_cuotas_idsocio(id)
 
    if cuotas != None:
        return jsonify(pagos_socio=[get_json(cuota) for cuota in cuotas])
    return jsonify("vacio")

@apis_blueprint.route("/<int:id>/payments", methods=["POST"])
#@apis_blueprint.route("/me/payments", methods=["POST"])
#@jwt_required()
def hacer_pago(id):
    # genera API POST de una cuota a pagar
    #id = get_jwt_identity()
    data = request.json

    mes = data["month"]
    importe = data["amount"]
    sinPagar = cuotaMethod.get_cuotas_nopagadas_socio(id)
    for cuota in sinPagar:
        if cuota.anomes.month == mes:
            if cuota.monto == importe:
                cuotaMethod.pago_cuota(cuota.id)
                return "success", 202
            return "monto diferente"
    return "salida"

@apis_blueprint.route("/me/license", methods=["GET"])
@jwt_required()
def mi_card():
    mi_id = get_jwt_identity()
    socio = socioMethod.get_socios_by_id(id=mi_id)
    if (socio.moroso):
        rta = "Tiene deuda pendiente."
    else:
        rta = "Cuotas al dìa."
    
    socio_json = {
        "name" : socio.nombre,
        "lastname" : socio.apellido,
        "email" : socio.email,
        "number" : socio.id,
        "document_type": socio.tipo_documento,
        "document_number": socio.documento,
        "gender": socio.genero,
        "address": socio.direccion,
        "phone": socio.telefono,
        "state": rta
    }

    return socio_json


@apis_blueprint.route("/estadistica/cant_socio_por_mes", methods=["GET"])
def cant_socio_por_mes():
    # genera API con la cantidad de cuotas generadas por mes
    
    def get_json(key, value):
        return {
            "mes": key,
            "cant_socios": value,
        }
    
    cuotas = cuotaMethod.get_cuotas()
    cuotas_por_mes = []
    [cuotas_por_mes.append(cuota.anomes.month) for cuota in cuotas]
    
    counts = dict(Counter(cuotas_por_mes))
    return jsonify([get_json(key, value) for key, value in counts.items()])

@apis_blueprint.route("/estadistica/dias_con_pagos", methods=["GET"])
def dias_con_pagos():
    # genera API los pagos realizados por día

    def get_json(key, value):
        return {
            "dia_pago": key,
            "cant_pagos": value,
        }

    cuotas = cuotaMethod.get_cuotas_pagadas()
    cuotas_pagadas = []
    [cuotas_pagadas.append(cuota.pagado_en.day) for cuota in cuotas]
    counts = dict(Counter(cuotas_pagadas))
    return jsonify([get_json(key, value) for key, value in counts.items()])

@apis_blueprint.route("/estadistica/socios_morosidad", methods=["GET"])
def socios_morosidad():
    # genera API con la cantidad de socio morosos y no morosos actuales
    
    def get_json(key, value):
        return {
            "status": key,
            "cant_socios": value,
        }

    socios = socioMethod.get_socios()
    socios_status = {
        'bloqueado':0,
        'moroso':0,
        'no_moroso':0
    }
    for socio in socios:
        if socio.estado:
            socios_status['bloqueado']+=1
        elif socio.moroso:
            socios_status['no_moroso']+=1
        else:
            socios_status['moroso']+=1
    return jsonify([get_json(key, value) for key, value in socios_status.items()])
