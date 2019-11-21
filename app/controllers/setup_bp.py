# -*- coding: utf-8 -*-
from flask import Blueprint, flash, redirect
from app import app
from app.ext.database import db
from sqlalchemy import exc
from app.models.banco.Usuario import Usuario
from app.models.banco.Produto import Produto
from hashlib import md5

setup_bp = Blueprint('setup', __name__, url_prefix='/setup')

@setup_bp.route('/')
def index():
    link_criar_tabelas = '<a href="/setup/create"> Criar tabelas </a>'
    link_deletar_tabelas = '<a href="/setup/drop"> Deletar tabelas </a>'
    link_popula_banco = '<a href="/setup/popula_banco"> Popular Banco </a>'

    return link_criar_tabelas + ' <br> ' + link_deletar_tabelas + ' <br> ' + link_popula_banco

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
    link_home_setup = '<a href="/setup"> Home setup </a>'

    senha1 = md5('admin'.encode())
    senha2 = md5('func'.encode())
    senha3 = md5('123'.encode())

    adm = Usuario(nome = 'Cleber', email = 'admin', senha = senha1.hexdigest(), cargo = 'administrador', endereco = 'Rua dos tolos, 0', cpf = '12345678998', data_nasc = '05/05/2005')
    func = Usuario(nome = 'Cleberson', email = 'func', senha = senha2.hexdigest(), cargo = 'funcionario', endereco = 'Rua dos tolos, 2', cpf = '1234567899', data_nasc = '06/06/2006')
    cliente = Usuario(nome = 'Jefferson', email = 'jef', senha = senha3.hexdigest(), cargo = 'cliente', endereco = 'Rua dos tolos, 3', cpf = '1234567890', data_nasc = '03/03/2003')

    for x in range(10):
        prod = Produto(nome = 'Produto {}'.format(x+1), descricao = "Produto {} muito bom".format(x+1), preco = (x+1)*100, quantidade = 2, arquivo = "uploads/85f97bbf-384a-4958-9490-a76ce8bc7762.png")
        db.session.add(prod)
        
    try:
        db.session.add(func)
        db.session.add(cliente)
        db.session.add(adm)
        db.session.commit()
        flash(u'Banco de dados populado com sucesso. Email: admin Senha: admin', 'success')

        return redirect('/produto')
    except exc.SQLAlchemyError:
        return 'Falha ao popular tableas <br> ' + link_home_setup