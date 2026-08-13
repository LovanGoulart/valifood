from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faça login para acessar esta página.'
    login_manager.login_message_category = 'warning'

    from app.routes import auth, dashboard, products, categories, notifications, api

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(categories.bp)
    app.register_blueprint(notifications.bp)
    app.register_blueprint(api.bp)

    with app.app_context():
        db.create_all()

        from app.models import Category, User

        if Category.query.count() == 0:
            default_cats = [
                ('Arroz e Grãos', '🍚'),
                ('Massas', '🍝'),
                ('Carnes', '🥩'),
                ('Laticínios', '🥛'),
                ('Bebidas', '🥤'),
                ('Frutas', '🍎'),
                ('Verduras e Legumes', '🥬'),
                ('Congelados', '🧊'),
                ('Enlatados', '🥫'),
                ('Doces', '🍬'),
                ('Temperos', '🌶️'),
                ('Produtos de Padaria', '🥖'),
                ('Outros', '📦')
            ]

            for name, icon in default_cats:
                db.session.add(
                    Category(name=name, icon=icon)
                )

            db.session.commit()

    return app