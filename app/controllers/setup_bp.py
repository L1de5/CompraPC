# -*- coding: utf-8 -*-
from flask import Blueprint
from app import app
from app.ext.database import db
from sqlalchemy import exc

setup_bp = Blueprint('setup', __name__, url_prefix='/setup')

@setup_bp.route('/')
def index():
    return '/create para criar tabelas <br> /drop para deletar tabelas'

@setup_bp.route('/create')
def create():
    try:
        with app.app_context():
            db.create_all()
        return 'Tabelas criadas com Sucesso'
    except exc.SQLAlchemyError:
        return 'Falha ao criar tabelas'

@setup_bp.route('/drop')
def drop():
    try:
        with app.app_context():
            db.drop_all()
        return 'Tabelas excluidas com Sucesso'
    except exc.SQLAlchemyError:
        return 'Falha ao excluir tableas'
