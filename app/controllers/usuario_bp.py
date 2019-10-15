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

                return redirect('/produtos')
            else:
                flash(u'Senha inválida!', 'danger')
        else:
            flash(u'Usuário inválido!', 'danger')

    return render_template('index.html', form = form, titulo = 'Logar')

@usuario_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()

    if request.method == "POST":
        nome = form.nome.data
        email = form.email.data
        senha = md5((form.senha.data).encode())
        endereco = form.endereco.data
        cpf = form.cpf.data
        dataNasc = '05/02/00'
        print(form.dataNasc.data)
        cliente = Cliente(nome = nome, email = email, senha = senha.hexdigest(), endereco = endereco, cpf = cpf, data_nasc = dataNasc)

        try:
            db.session.add(cliente)
            db.session.commit()
            #login_usuario(new_user) Explica ai

            return redirect('/produtos')
        except exc.SQLAlchemyError:
            flash(u'Ocorreu um problema ao tentar cadastrar usuário, tente novamente!', 'danger')

            return render_template('index.html', form=form, titulo='Cadastrar')

    return render_template('index.html', form=form, titulo='Cadastrar')

@usuario_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/produtos')
