import os

SECRET_KEY = os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'FYYUR_DATABASE_URI',
    'postgresql+psycopg://postgres:postgres@localhost:5433/fyyurdb',
)
