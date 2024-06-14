from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash

db = SQLAlchemy()

class TipoUsuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    usuarios = db.relationship('User', backref='tipo_usuario', lazy=True)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    tipo_usuario_id = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id'), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf8')
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    stock_total = db.Column(db.Integer, nullable=False)
    almacen_id = db.Column(db.Integer, db.ForeignKey('almacen.id'), nullable=False)

class Almacen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

class ProductoAlmacen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    almacen_id = db.Column(db.Integer, db.ForeignKey('almacen.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    correo = db.Column(db.String(150), nullable=False)

class Insumos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    almacen_id = db.Column(db.Integer, db.ForeignKey('almacen.id'), nullable=False)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_nombre = db.Column(db.String(50), nullable=False)
    cliente_apellido = db.Column(db.String(50), nullable=False)
    cliente_documento = db.Column(db.String(20), nullable=False)
    cliente_direccion = db.Column(db.String(200), nullable=False)

class Pedidos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

class Ventas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    saldo_total = db.Column(db.Float, nullable=False)

class InsumosAlmacen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False)
    almacen_id = db.Column(db.Integer, db.ForeignKey('almacen.id'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)