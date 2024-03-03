from flask import Flask, jsonify, request, Blueprint
import uuid
from datetime import datetime

from ..utils.utils import is_email
from ..commands.create import CreateUser
from ..commands.exists import ExistsUser
from ..commands.update import UpdateUser
from ..commands.get import GetUser
from ..commands.reset import ResetDB
from ..commands.token import CreateToken

import os

operations_blueprint = Blueprint('operations', __name__)

@operations_blueprint.route('/users', methods = ['POST'])
def create():
    json = request.get_json()
    username = json.get('username')
    password = json.get('password')
    email = json.get('email')

    #Valido los campos 
    if not username or not password  or not email:
        return "", 400
    if not is_email(email):
        return "Campo email no válido", 400
    
    dni = json.get('dni')
    if dni is not None and not dni.isdigit():
        return "Campo dni no válido", 400
    
    phoneNumber = json.get('phoneNumber')
    if dni is not None and not phoneNumber.isdigit():
        return "Campo phoneNumber no válido", 400
    
    fullName = json.get('fullName')

    #Verifico si el usuario ya existe
    if ExistsUser(id=None, username=username, email=email).execute():
        return "El username o email ya está en uso", 412

    #Almaceno el usuario
    user = CreateUser(username, password, email, fullName, dni, phoneNumber).execute()
    
    return jsonify({
        "id": user.id,
        "createdAt": user.createdAt
    }), 201

@operations_blueprint.route('/users/<user_id>', methods = ['PATCH'])
def update(user_id):
    json = request.get_json()

    fullName = json.get('fullName')
    phoneNumber = json.get('phoneNumber')
    dni = json.get('dni')
    status = json.get('status')

    if not fullName and not phoneNumber and not dni and not status:
        return "No hay campos para actualizar", 400
    
    #Verifico si el usuario existe
    if not ExistsUser(id=user_id).execute():
        return "El usuario no existe", 404
    
    #Update user
    UpdateUser(id=user_id, fullName=fullName, phoneNumber=phoneNumber, dni=dni, status=status).execute()
    
    return jsonify({
        "msg": "el usuario ha sido actualizado"
    })

@operations_blueprint.route('/users/auth', methods = ['POST'])
def auth():
    json = request.get_json()
    username = json.get('username')
    password = json.get('password')
    
    if not username and not password:
        return "", 404
    
    if not username or not password:
        return "", 400
    
    token = CreateToken(username, password).execute()
    if token is None:
        return "", 404

    return jsonify(token)

@operations_blueprint.route('/users/me', methods = ['GET'])
def get():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return "", 403
    
    user = GetUser(auth_header[7:]).execute()
    if user is None:
        return "", 401
    
    dni = user.dni
    if dni is not None and dni.isdigit() or len(auth_header) < 10:
        dni = int(dni)

    phoneNumber = user.phoneNumber
    if phoneNumber is not None and phoneNumber.isdigit():
        phoneNumber = int(phoneNumber)
    
    return jsonify({
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "fullName": user.fullName,
        "dni": dni,
        "phoneNumber": phoneNumber,
        "status": user.status
    })
 
@operations_blueprint.route('/users/ping', methods = ['GET'])
def ping():
    return "pong"

@operations_blueprint.route('/users/reset', methods = ['POST'])
def reset():
    ResetDB().execute()

    return jsonify({"msg": "Todos los datos fueron eliminados"})
 