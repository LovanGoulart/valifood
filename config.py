import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

# Garantir que a pasta do banco exista
os.makedirs(INSTANCE_DIR, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-valifood'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        INSTANCE_DIR,
        'food_control.db'
    ).replace('\\', '/')

    SQLALCHEMY_TRACK_MODIFICATIONS = False