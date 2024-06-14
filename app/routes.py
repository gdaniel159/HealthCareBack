from flask import Blueprint, request, jsonify
from app.models import User, db, TipoUsuario, Producto, Almacen, ProductoAlmacen, Categoria, Proveedor, Insumos, Cliente, Pedidos, Ventas, InsumosAlmacen
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

@main.route('/api/product', methods=['GET'])
@jwt_required()

def get_products():
    products = Producto.query.all()
    products_list = [
        {"id":product.id, "nombre":product.nombre, "categoria_id" : product.categoria_id, "stock_total":product.stock_total} for product in products
    ]
    return jsonify(products_list)

@main.route('/api/almacen', methods=['GET'])
@jwt_required()
def get_almacenes():
    almacenes = Almacen.query.all()
    almacen_list = [{"id": almacen.id, "nombre": almacen.nombre} for almacen in almacenes]
    return jsonify(almacen_list)

@main.route('/api/producto_almacen', methods=['GET'])
@jwt_required()
def get_producto_almacen():
    productos_almacen = ProductoAlmacen.query.all()
    producto_almacen_list = [{"id": pa.id, "almacen_id": pa.almacen_id, "producto_id": pa.producto_id, "stock": pa.stock} for pa in productos_almacen]
    return jsonify(producto_almacen_list)

@main.route('/api/categoria', methods=['GET'])
@jwt_required()
def get_categorias():
    categorias = Categoria.query.all()
    categoria_list = [{"id": categoria.id, "nombre": categoria.nombre} for categoria in categorias]
    return jsonify(categoria_list)

@main.route('/api/proveedor', methods=['GET'])
@jwt_required()
def get_proveedores():
    proveedores = Proveedor.query.all()
    proveedor_list = [{"id": proveedor.id, "nombre": proveedor.nombre, "telefono": proveedor.telefono, "direccion": proveedor.direccion, "correo": proveedor.correo} for proveedor in proveedores]
    return jsonify(proveedor_list)

@main.route('/api/insumos', methods=['GET'])
@jwt_required()
def get_insumos():
    insumos = Insumos.query.all()
    insumos_list = [{"id": insumo.id, "nombre": insumo.nombre, "proveedor_id": insumo.proveedor_id, "stock": insumo.stock} for insumo in insumos]
    return jsonify(insumos_list)

@main.route('/api/cliente', methods=['GET'])
@jwt_required()
def get_clientes():
    clientes = Cliente.query.all()
    cliente_list = [{"id": cliente.id, "cliente_nombre": cliente.cliente_nombre, "cliente_apellido": cliente.cliente_apellido, "cliente_documento": cliente.cliente_documento, "cliente_direccion": cliente.cliente_direccion} for cliente in clientes]
    return jsonify(cliente_list)

@main.route('/api/pedidos', methods=['GET'])
@jwt_required()
def get_pedidos():
    pedidos = Pedidos.query.all()
    pedidos_list = [{"id": pedido.id, "producto_id": pedido.producto_id, "cliente_id": pedido.cliente_id, "cantidad": pedido.cantidad} for pedido in pedidos]
    return jsonify(pedidos_list)

@main.route('/api/ventas', methods=['GET'])
@jwt_required()
def get_ventas():
    ventas = Ventas.query.all()
    ventas_list = [{"id": venta.id, "pedido_id": venta.pedido_id, "saldo_total": venta.saldo_total} for venta in ventas]
    return jsonify(ventas_list)

@main.route('/api/insumos_almacen', methods=['GET'])
@jwt_required()
def get_insumos_almacen():
    insumos_almacen = InsumosAlmacen.query.all()
    insumos_almacen_list = [{"id": ia.id, "insumo_id": ia.insumo_id, "almacen_id": ia.almacen_id, "stock": ia.stock} for ia in insumos_almacen]
    return jsonify(insumos_almacen_list)

# POST

@main.route('/api/insumos_almacen', methods=['POST'])
@jwt_required()
def create_insumos_almacen():
    data = request.get_json()
    new_insumos_almacen = InsumosAlmacen(insumo_id=data['insumo_id'], almacen_id=data['almacen_id'], stock=data['stock'])
    db.session.add(new_insumos_almacen)
    db.session.commit()
    return jsonify({"message": "Insumo en almacén creado exitosamente"}), 201

@main.route('/api/ventas', methods=['POST'])
@jwt_required()
def create_venta():
    data = request.get_json()
    new_venta = Ventas(pedido_id=data['pedido_id'], saldo_total=data['saldo_total'])
    db.session.add(new_venta)
    db.session.commit()
    return jsonify({"message": "Venta creada exitosamente"}), 201

@main.route('/api/pedidos', methods=['POST'])
@jwt_required()
def create_pedido():
    data = request.get_json()
    new_pedido = Pedidos(producto_id=data['producto_id'], cliente_id=data['cliente_id'], cantidad=data['cantidad'])
    db.session.add(new_pedido)
    db.session.commit()
    return jsonify({"message": "Pedido creado exitosamente"}), 201

@main.route('/api/cliente', methods=['POST'])
@jwt_required()
def create_cliente():
    data = request.get_json()
    new_cliente = Cliente(cliente_nombre=data['cliente_nombre'], cliente_apellido=data['cliente_apellido'], cliente_documento=data['cliente_documento'], cliente_direccion=data['cliente_direccion'])
    db.session.add(new_cliente)
    db.session.commit()
    return jsonify({"message": "Cliente creado exitosamente"}), 201

@main.route('/api/insumos', methods=['POST'])
@jwt_required()
def create_insumos():
    data = request.get_json()
    
    # Crear el nuevo insumo
    new_insumo = Insumos(nombre=data['nombre'], proveedor_id=data['proveedor_id'], stock=data['stock'], almacen_id=data['almacen_id'])
    db.session.add(new_insumo)
    db.session.commit()

    # Asociar el nuevo insumo al almacén especificado con un stock inicial de 0
    insumo_almacen = InsumosAlmacen(insumo_id=new_insumo.id, almacen_id=new_insumo.almacen_id, stock=new_insumo.stock)
    db.session.add(insumo_almacen)
    db.session.commit()

    return jsonify({'message': "Insumo creado correctamente"})

@main.route('/api/proveedor', methods=['POST'])
@jwt_required()
def create_proveedor():
    data = request.get_json()
    new_proveedor = Proveedor(nombre=data['nombre'], telefono=data['telefono'], direccion=data['direccion'], correo=data['correo'])
    db.session.add(new_proveedor)
    db.session.commit()
    return jsonify({"message": "Proveedor creado exitosamente"}), 201

@main.route('/api/categoria', methods=['POST'])
@jwt_required()
def create_categoria():
    data = request.get_json()
    new_categoria = Categoria(nombre=data['nombre'])
    db.session.add(new_categoria)
    db.session.commit()
    return jsonify({"message": "Categoría creada exitosamente"}), 201

@main.route('/api/producto_almacen', methods=['POST'])
@jwt_required()
def create_producto_almacen():
    data = request.get_json()
    new_producto_almacen = ProductoAlmacen(almacen_id=data['almacen_id'], producto_id=data['producto_id'], stock=data['stock'])
    db.session.add(new_producto_almacen)
    db.session.commit()
    return jsonify({"message": "Producto en almacén creado exitosamente"}), 201

@main.route('/api/almacen', methods=['POST'])
@jwt_required()
def create_almacen():
    data = request.get_json()
    new_almacen = Almacen(nombre=data['nombre'])
    db.session.add(new_almacen)
    db.session.commit()
    return jsonify({"message": "Almacén creado exitosamente"}), 201

@main.route('/api/product', methods=['POST'])
@jwt_required()

def store_product():

    data = request.get_json()
    
    existing_products = Producto.query.filter_by(nombre=data['nombre']).first()

    if existing_products:
        return jsonify({'message':'El producto ya existe'}), 400
    
    new_product = Producto(nombre=data['nombre'], categoria_id=data['categoria_id'], stock_total=data['stock_total'], almacen_id=data['almacen_id'])
    db.session.add(new_product)
    db.session.commit()

    # Asociar el nuevo insumo al almacén especificado con un stock inicial de 0
    producto_almacen = ProductoAlmacen(almacen_id=new_product.almacen_id, stock=new_product.stock_total, producto_id=new_product.id)
    db.session.add(producto_almacen)
    db.session.commit()

    return jsonify({'message': "Insumo creado correctamente"})

@main.route('/api/tipo_usuario', methods=['POST'])
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

@main.route('/api/insumos_almacen/<int:id>', methods=['PUT'])
@jwt_required()
def update_insumos_almacen(id):
    data = request.get_json()
    insumo_almacen = InsumosAlmacen.query.get(id)
    if not insumo_almacen:
        return jsonify({"message": "Insumo en almacén no encontrado"}), 404
    insumo_almacen.insumo_id = data.get('insumo_id', insumo_almacen.insumo_id)
    insumo_almacen.almacen_id = data.get('almacen_id', insumo_almacen.almacen_id)
    insumo_almacen.stock = data.get('stock', insumo_almacen.stock)
    db.session.commit()
    return jsonify({"message": "Insumo en almacén actualizado exitosamente"})

@main.route('/api/ventas/<int:id>', methods=['PUT'])
@jwt_required()
def update_venta(id):
    data = request.get_json()
    venta = Ventas.query.get(id)
    if not venta:
        return jsonify({"message": "Venta no encontrada"}), 404
    venta.pedido_id = data.get('pedido_id', venta.pedido_id)
    venta.saldo_total = data.get('saldo_total', venta.saldo_total)
    db.session.commit()
    return jsonify({"message": "Venta actualizada exitosamente"})

@main.route('/api/pedidos/<int:id>', methods=['PUT'])
@jwt_required()
def update_pedido(id):
    data = request.get_json()
    pedido = Pedidos.query.get(id)
    if not pedido:
        return jsonify({"message": "Pedido no encontrado"}), 404
    pedido.producto_id = data.get('producto_id', pedido.producto_id)
    pedido.cliente_id = data.get('cliente_id', pedido.cliente_id)
    pedido.cantidad = data.get('cantidad', pedido.cantidad)
    db.session.commit()
    return jsonify({"message": "Pedido actualizado exitosamente"})

@main.route('/api/cliente/<int:id>', methods=['PUT'])
@jwt_required()
def update_cliente(id):
    data = request.get_json()
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"message": "Cliente no encontrado"}), 404
    cliente.cliente_nombre = data.get('cliente_nombre', cliente.cliente_nombre)
    cliente.cliente_apellido = data.get('cliente_apellido', cliente.cliente_apellido)
    cliente.cliente_documento = data.get('cliente_documento', cliente.cliente_documento)
    cliente.cliente_direccion = data.get('cliente_direccion', cliente.cliente_direccion)
    db.session.commit()
    return jsonify({"message": "Cliente actualizado exitosamente"})

@main.route('/api/insumos/<int:id>', methods=['PUT'])
@jwt_required()
def update_insumos(id):
    data = request.get_json()
    insumo = Insumos.query.get(id)
    if not insumo:
        return jsonify({"message": "Insumo no encontrado"}), 404
    insumo.nombre = data.get('nombre', insumo.nombre)
    insumo.proveedor_id = data.get('proveedor_id', insumo.proveedor_id)
    insumo.stock = data.get('stock', insumo.stock)
    db.session.commit()
    return jsonify({"message": "Insumo actualizado exitosamente"})

@main.route('/api/proveedor/<int:id>', methods=['PUT'])
@jwt_required()
def update_proveedor(id):
    data = request.get_json()
    proveedor = Proveedor.query.get(id)
    if not proveedor:
        return jsonify({"message": "Proveedor no encontrado"}), 404
    proveedor.nombre = data.get('nombre', proveedor.nombre)
    proveedor.telefono = data.get('telefono', proveedor.telefono)
    proveedor.direccion = data.get('direccion', proveedor.direccion)
    proveedor.correo = data.get('correo', proveedor.correo)
    db.session.commit()
    return jsonify({"message": "Proveedor actualizado exitosamente"})

@main.route('/api/categoria/<int:id>', methods=['PUT'])
@jwt_required()
def update_categoria(id):
    data = request.get_json()
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({"message": "Categoría no encontrada"}), 404
    categoria.nombre = data.get('nombre', categoria.nombre)
    db.session.commit()
    return jsonify({"message": "Categoría actualizada exitosamente"})

@main.route('/api/producto_almacen/<int:id>', methods=['PUT'])
@jwt_required()
def update_producto_almacen(id):
    data = request.get_json()
    producto_almacen = ProductoAlmacen.query.get(id)
    if not producto_almacen:
        return jsonify({"message": "Producto en almacén no encontrado"}), 404
    producto_almacen.almacen_id = data.get('almacen_id', producto_almacen.almacen_id)
    producto_almacen.producto_id = data.get('producto_id', producto_almacen.producto_id)
    producto_almacen.stock = data.get('stock', producto_almacen.stock)
    db.session.commit()
    return jsonify({"message": "Producto en almacén actualizado exitosamente"})

@main.route('/api/almacen/<int:id>', methods=['PUT'])
@jwt_required()
def update_almacen(id):
    data = request.get_json()
    almacen = Almacen.query.get(id)
    if not almacen:
        return jsonify({"message": "Almacén no encontrado"}), 404
    almacen.nombre = data.get('nombre', almacen.nombre)
    db.session.commit()
    return jsonify({"message": "Almacén actualizado exitosamente"})

@main.route('/api/user/<int:id>', methods=['PUT'])
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

@main.route('/api/insumos_almacen/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_insumos_almacen(id):
    insumo_almacen = InsumosAlmacen.query.get(id)
    if not insumo_almacen:
        return jsonify({"message": "Insumo en almacén no encontrado"}), 404
    db.session.delete(insumo_almacen)
    db.session.commit()
    return jsonify({"message": "Insumo en almacén eliminado exitosamente"})

@main.route('/api/ventas/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_venta(id):
    venta = Ventas.query.get(id)
    if not venta:
        return jsonify({"message": "Venta no encontrada"}), 404
    db.session.delete(venta)
    db.session.commit()
    return jsonify({"message": "Venta eliminada exitosamente"})

@main.route('/api/pedidos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_pedido(id):
    pedido = Pedidos.query.get(id)
    if not pedido:
        return jsonify({"message": "Pedido no encontrado"}), 404
    db.session.delete(pedido)
    db.session.commit()
    return jsonify({"message": "Pedido eliminado exitosamente"})

@main.route('/api/cliente/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({"message": "Cliente no encontrado"}), 404
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente eliminado exitosamente"})

@main.route('/api/insumos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_insumos(id):
    insumo = Insumos.query.get(id)
    if not insumo:
        return jsonify({"message": "Insumo no encontrado"}), 404
    db.session.delete(insumo)
    db.session.commit()
    return jsonify({"message": "Insumo eliminado exitosamente"})

@main.route('/api/proveedor/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_proveedor(id):
    proveedor = Proveedor.query.get(id)
    if not proveedor:
        return jsonify({"message": "Proveedor no encontrado"}), 404
    db.session.delete(proveedor)
    db.session.commit()
    return jsonify({"message": "Proveedor eliminado exitosamente"})

@main.route('/api/categoria/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({"message": "Categoría no encontrada"}), 404
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({"message": "Categoría eliminada exitosamente"})

@main.route('/api/producto_almacen/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_producto_almacen(id):
    producto_almacen = ProductoAlmacen.query.get(id)
    if not producto_almacen:
        return jsonify({"message": "Producto en almacén no encontrado"}), 404
    db.session.delete(producto_almacen)
    db.session.commit()
    return jsonify({"message": "Producto en almacén eliminado exitosamente"})

@main.route('/api/almacen/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_almacen(id):
    almacen = Almacen.query.get(id)
    if not almacen:
        return jsonify({"message": "Almacén no encontrado"}), 404
    db.session.delete(almacen)
    db.session.commit()
    return jsonify({"message": "Almacén eliminado exitosamente"})

@main.route('/api/user/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado correctamente"})

@main.route('/api/productos_por_almacen/<int:almacen_id>', methods=['GET'])
@jwt_required()
def productos_por_almacen(almacen_id):
    # Buscar el almacén por su ID
    almacen = Almacen.query.get_or_404(almacen_id)

    if almacen_id == 1:
        # Si es el almacén 1, obtener los productos almacenados
        productos_almacen = ProductoAlmacen.query.filter_by(almacen_id=almacen_id).all()

        # Crear una lista para almacenar los datos de los productos
        productos_list = []

        # Recorrer los productos del almacén y obtener la información necesaria
        for producto_almacen in productos_almacen:
            producto = Producto.query.get(producto_almacen.producto_id)
            if producto:
                productos_list.append({
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'stock': producto_almacen.stock
                })

        return jsonify(productos_list)
    elif almacen_id == 2:
        # Si es el almacén 2, obtener los insumos almacenados
        insumos_almacen = InsumosAlmacen.query.filter_by(almacen_id=almacen_id).all()

        # Crear una lista para almacenar los datos de los insumos
        insumos_list = []

        # Recorrer los insumos del almacén y obtener la información necesaria
        for insumo_almacen in insumos_almacen:
            insumo = Insumos.query.get(insumo_almacen.insumo_id)
            if insumo:
                insumos_list.append({
                    'id': insumo.id,
                    'nombre': insumo.nombre,
                    'stock': insumo_almacen.stock
                })

        return jsonify(insumos_list)
    else:
        return jsonify({'message': 'Almacén no encontrado'})