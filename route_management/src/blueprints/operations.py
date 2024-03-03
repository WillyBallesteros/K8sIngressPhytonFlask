from datetime import datetime, timezone 
import re
from flask import Flask, jsonify, request, Blueprint
from ..commands.create import CreateFlight
from ..commands.exists import ExistsFlight
from ..commands.query import QueryRoute
from ..commands.delete import DeleteRoute
from ..commands.reset import ResetRoute
from ..utils.utils import get_info_token, is_uuid_valid
import logging
import sys


operations_blueprint = Blueprint('operations', __name__)

# Configurar el nivel de logging
logging.basicConfig(level=logging.WARNING)
# Crear un objeto logger
logger = logging.getLogger(__name__)
# Agregar un StreamHandler para enviar los registros a la salida estándar (stdout)
logger.addHandler(logging.StreamHandler(sys.stdout))

def common_validations(auth_header):
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return 403
   
    info_token = get_info_token(auth_header)
    if not info_token:
        return 401

@operations_blueprint.route('/routes/reset', methods = ['POST'])
def reset():
    ResetRoute().execute()

    return jsonify({"msg": "Todos los datos fueron eliminados"})

@operations_blueprint.route('/routes', methods = ['POST'])
def create():
    logging.warning("ROUTESSSS")
    json = request.get_json()
    
    # Extraer los valores de los campos
    flightId = json.get('flightId')
    sourceAirportCode = json.get('sourceAirportCode')
    sourceCountry = json.get('sourceCountry')
    destinyAirportCode = json.get('destinyAirportCode')
    destinyCountry = json.get('destinyCountry')
    bagCost = json.get('bagCost')
    plannedStartDate = json.get('plannedStartDate')
    plannedEndDate = json.get('plannedEndDate')

    # Verificar si alguno de los valores extraídos es None (campo faltante)
    if None in [flightId, sourceAirportCode, sourceCountry, destinyAirportCode, destinyCountry, bagCost, plannedStartDate, plannedEndDate]:
        # Devolver un error si algún campo está faltando
        return jsonify({"error": "Faltan uno o más campos requeridos"}), 400
    
    auth_header = request.headers.get('Authorization')
    validations = common_validations(auth_header)
    if validations:
         return "", validations
    
    # Verifico que el trayecto no exista
    flightId = json.get('flightId')
    if ExistsFlight(flightId).execute():
        return jsonify({"error": "Ya existe un trayecto registrado con ese flightId"}), 412
    
    logging.warning(f"plannedStartDate {plannedStartDate}")
    logging.warning(f"plannedEndDate   {plannedEndDate}")
    
    # Verifica que las fechas tengan el formato correcto    
    start_date = datetime.fromisoformat(plannedStartDate.replace('Z', '+00:00'))
    end_date = datetime.fromisoformat(plannedEndDate.replace('Z', '+00:00'))    
    
    # Obtiene la fecha y hora actual
    now = datetime.now(timezone.utc)
    logging.warning(f"start_date {start_date}")
    logging.warning(f"end_date   {end_date}")
    logging.warning(f"now        {now}")
    # Verifica que las fechas no estén en el pasado
    if start_date  < now or end_date  < now:
        return jsonify({"msg": "Las fechas del trayecto no son válidas"}), 412
    
    # Asegura que la fecha de fin sea igual o posterior a la fecha de inicio
    if end_date  < start_date :
        return jsonify({"msg": "Las fechas del trayecto no son válidas"}), 412    

    # Almaceno el trayecto
    flight = CreateFlight(flightId, sourceAirportCode, sourceCountry, destinyAirportCode, destinyCountry, bagCost, plannedStartDate, plannedEndDate).execute()
    
    return jsonify({
        "id": flight.id,
        "createdAt": flight.createdAt
    }), 201

@operations_blueprint.route('/routes/ping', methods = ['GET'])
def ping():
    return "pong"

@operations_blueprint.route('/routes', methods=['GET'])
def get_routes():
    
    # Obtener los parámetros de la solicitud
    flightId = request.args.get('flight')
    id = request.args.get('id')
    auth_header = request.headers.get('Authorization')

    validations = common_validations(auth_header)
    if validations:
         return "", validations
    
    flights = QueryRoute(flight_id=flightId, id=id).execute()
    return flights

@operations_blueprint.route('/routes/<string:id>', methods=['GET'])
def get_routes_id(id):

    auth_header = request.headers.get('Authorization')
    validations = common_validations(auth_header)
    if validations:
         return "", validations
    
    #Validar uuid
    if not is_uuid_valid(id) :
        return "", 400
    
    routes = QueryRoute(id=id).execute()

    route = routes.get_json()
    if not len(route) > 0:
         return '', 404
    
    return route[0]

@operations_blueprint.route('/routes/<string:id>', methods=['DELETE'])
def delete_route(id):
    auth_header = request.headers.get('Authorization')
    validations = common_validations(auth_header)
    if validations:
         return "", validations
    
    if not is_uuid_valid(id) :
        return "", 400
    
    execute = DeleteRoute(id).execute()
    if execute == 200:
        return {"msg": "el trayecto fue eliminado"}, execute
    else:
         return '', execute