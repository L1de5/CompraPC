# -*- coding: utf-8 -*-
from flask import Blueprint, flash, redirect
from app import app
from app.ext.database import db
from sqlalchemy import exc
from app.models.banco.Usuario import Usuario
from hashlib import md5

setup_bp = Blueprint('setup', __name__, url_prefix='/setup')

@setup_bp.route('/')
def index():
    link_criar_tabelas = '<a href="/setup/create"> Criar tabelas </a>'
    link_deletar_tabelas = '<a href="/setup/drop"> Deletar tabelas </a>'

    return link_criar_tabelas + ' <br> ' + link_deletar_tabelas

@setup_bp.route('/create')
def create():
    link_home_setup = '<a href="/setup"> Home setup </a>'

    try:
        with app.app_context():
            db.create_all()
        return 'Tabelas criadas com sucesso <br> ' + link_home_setup
    except exc.SQLAlchemyError:
        return 'Falha ao criar tabelas <br> ' + link_home_setup

@setup_bp.route('/drop')
def drop():
    link_home_setup = '<a href="/setup"> Home setup </a>'
    
    try:
        with app.app_context():
            db.drop_all()
        return 'Tabelas excluidas com sucesso <br> ' + link_home_setup
    except exc.SQLAlchemyError:
        return 'Falha ao excluir tableas <br> ' + link_home_setup

@setup_bp.route('/popula_banco')
def popula_banco():
    adm = Usuario(nome = 'Cleber', email = 'admin', senha = senha.hexdigest(), endereco = endereco, cpf = cpf, data_nasc = data_nasc)
    
    try:

        db.session.add(produto)
        db.session.commit()
        flash(u'Banco de dados populado com sucesso <br> ADM Email: adm@email.com Senha: adm123', 'danger')

        return redirect('/produto')
    except exc.SQLAlchemyError:
        return 'Falha ao popular tableas <br> ' + link_home_setup