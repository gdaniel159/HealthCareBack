from flask import Flask
from app.config import Config
from app.models import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .seeders import seed_tipos_usuarios, seed_usuarios, seed_almacenes, seed_categorias

bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Configuraciones
    app.config.from_object(Config)

    # Inicializar la base de datos
    db.init_app(app)

    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}) # Habilitar el cors para rutas externas

    with app.app_context():
        db.create_all()
        seed_tipos_usuarios()
        seed_usuarios()
        seed_almacenes()
        seed_categorias()

    # Registro de las rutas
    from app.routes import main
    app.register_blueprint(main)

    return app
