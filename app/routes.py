from flask import Blueprint, request, jsonify
from app.models import User, db, TipoUsuario
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta

main = Blueprint('main', __name__)

# Test Route

@main.route('/')
def home():
    return jsonify({"message": "¡Hola, Mundo!"})

# GET

@main.route('/api/users', methods=['GET'])
@jwt_required()

def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(user_list)

@main.route('/api/tipo_usuarios', methods=['GET'])
@jwt_required()

def get_type_users():
    type_user = TipoUsuario.query.all()
    type_user_list = [
        {"id":type.id, "nombre":type.nombre} for type in type_user
    ]
    return jsonify(type_user_list)

# POST

@main.route('/api/tipo_usuario/create', methods=['POST'])
def store_tipo_usuario():
    data = request.get_json()
    existing_type_user = TipoUsuario.query.filter_by(nombre=data['nombre']).first()

    if existing_type_user:
        return jsonify({"message":"El tipo de usuario ya existe"}), 400
    
    new_type_user = TipoUsuario(nombre=data['nombre'])
    db.session.add(new_type_user)
    db.session.commit()
    return jsonify({'message':"Tipo de usuario registrado correctamente"}), 201

@main.route('/api/user/register', methods=['POST'])
def register_user():
    data = request.get_json()
    existing_user = User.query.filter_by(email=data['email']).first()
    
    if existing_user:
        return jsonify({"message": "El usuario ingresado ya existe"}), 400

    new_user = User(username=data['username'], email=data['email'], password=data['password'], tipo_usuario_id=data['tipo_usuario_id'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuarios registrado correctamente"}), 201

@main.route('/api/user/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.verify_password(data['password']):
        return jsonify({"message": "Correo y contraseña incorrectos"}), 401

    access_token = create_access_token(identity={'username': user.username, 'email': user.email}, expires_delta=timedelta(hours=1))
    
    response = {
        "message": "Inicio de sesión exitoso",
        "access_token": access_token,
        "tipo_usuario": user.tipo_usuario.id
    }

    return jsonify(response), 200

# PUT

@main.route('/api/user/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    
    if not user:
        return jsonify({"message":"Usuario no encontrado"}), 404
    
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)

    db.session.commit()
    return jsonify({"message":"Usuario actualizado correctame"})

# DELETE

@main.route('/api/user/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado correctamente"})