# -*- coding: utf-8 -*-
from app import app
from flask import render_template, request, Blueprint, redirect, flash
from app.models.form.cadastro_usuario import CadastroForm
from app.models.form.login_usuario import LoginForm
from app.models.banco.Cliente import Cliente
from app.ext.database import db
from flask_login import login_user, login_required, logout_user
from hashlib import md5
from sqlalchemy import exc

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    db.create_all()
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        senha = md5(form.senha.data.encode())
        cliente = Cliente.query.filter_by(email = email).first()

        if cliente:
            if cliente.senha == senha.hexdigest():
                login_user(cliente)
            else:
                flash(u'Senha inválida!', 'danger')
        else:
            flash(u'Usuário inválido!', 'danger')

    return redirect('/produto')

@usuario_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = md5((request.form['senha']).encode())
        conf_senha = md5((request.form['conf_senha']).encode())
        endereco = request.form['endereco']
        cpf = request.form['cpf']
        data_nasc = request.form['data_nasc']
        
        if senha.hexdigest() == conf_senha.hexdigest():
            try:
                new_cliente = Cliente(nome = nome, email = email, senha = senha.hexdigest(), endereco = endereco, cpf = cpf, data_nasc = data_nasc)
                db.session.add(new_cliente)
                db.session.commit()
                login_user(new_cliente)
            except exc.SQLAlchemyError:
                flash(u'Ocorreu um problema ao tentar cadastrar usuário, tente novamente!', 'danger')
        else:
            flash(u'Ocorreu um problema ao tentar cadastrar usuário, as senhas não coincidem!', 'danger')

    return redirect('/produto')

@usuario_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/produto')
