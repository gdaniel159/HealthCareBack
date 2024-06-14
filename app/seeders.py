from flask import current_app
from .models import db, TipoUsuario, User, Almacen, Categoria

def seed_tipos_usuarios():
    with current_app.app_context():
        # Comprobar si ya hay tipos de usuarios en la base de datos
        if TipoUsuario.query.count() > 0:
            print("Ya existen tipos de usuarios en la base de datos. No es necesario sembrar.")
            return
        
        # Sembrar tipos de usuarios en la base de datos
        tipos_usuarios_data = [
            {"nombre": "Administrador"},
            # Agrega más tipos de usuarios según sea necesario
        ]
        
        for tipo_usuario_data in tipos_usuarios_data:
            tipo_usuario = TipoUsuario(**tipo_usuario_data)
            db.session.add(tipo_usuario)
        db.session.commit()

def seed_usuarios():
    with current_app.app_context():
        # Comprobar si ya hay usuarios en la base de datos
        if User.query.count() > 0:
            print("Ya existen usuarios en la base de datos. No es necesario sembrar.")
            return
        
        # Sembrar usuarios en la base de datos
        usuarios_data = [
            {"username": "GDaniel12", "email": "german.sc937@gmail.com", "password": "1234", "tipo_usuario_id": "1"}
        ]
        
        for usuario_data in usuarios_data:
            user = User(**usuario_data)
            db.session.add(user)
        db.session.commit()

def seed_almacenes():
    with current_app.app_context():
        # Comprobar si ya hay almacenes en la base de datos
        if Almacen.query.count() > 0:
            print("Ya existen almacenes en la base de datos. No es necesario sembrar.")
            return
        
        # Sembrar almacenes en la base de datos
        almacenes_data = [
            {"nombre": "Almacén 1"},
            {"nombre": "Almacén 2"},
            # Agrega más almacenes según sea necesario
        ]
        
        for almacen_data in almacenes_data:
            almacen = Almacen(**almacen_data)
            db.session.add(almacen)
        db.session.commit()

def seed_categorias():
    with current_app.app_context():
        # Comprobar si ya hay categorías en la base de datos
        if Categoria.query.count() > 0:
            print("Ya existen categorías en la base de datos. No es necesario sembrar.")
            return
        
        # Sembrar categorías en la base de datos
        categorias_data = [
            {"nombre": "Categoría 1"},
            {"nombre": "Categoría 2"},
            # Agrega más categorías según sea necesario
        ]
        
        for categoria_data in categorias_data:
            categoria = Categoria(**categoria_data)
            db.session.add(categoria)
        db.session.commit()