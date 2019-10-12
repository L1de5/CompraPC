# -*- coding: utf-8 -*-
from flask import render_template, request, Blueprint, redirect, url_for, flash
from app.models.form.cadastro_usuario import CadastroForm
from app.models.form.login_usuario import LoginForm
from app.models.banco.Cliente import Cliente
from app.ext.database import db
from app.ext.login import login_mananger
from flask_login import login_user, login_required, logout_user, current_user
from hashlib import md5
from sqlalchemy import exc

home_bp = Blueprint('home', __name__, url_prefix='/home')

@home_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        senha = md5(form.senha.data.encode())
        cliente = Cliente.query.filter_by(email = email).first()

        if cliente:
            if cliente.senha == senha.hexdigest():
                login_user(cliente)

                return 'aeeeee'
            else:
                flash(u'Senha inválida!', 'danger')
        else:
            flash(u'Usuário inválido!', 'danger')

    return render_template('index.html', form = form, titulo = 'Logar')

@home_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()

    if form.validate_on_submit():
        username = form.username.data
        login = form.login.data
        email = form.email.data
        password = form.password.data
        idade = form.idade.data
        altura = form.altura.data
        new_user = User(nome = username, login = login, email = email, senha = password, idade = idade, altura = altura)

        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            return redirect('/series')
        except exc.SQLAlchemyError:
            flash(u'Ocorreu um problema ao tentar cadastrar usuário, tente novamente!', 'danger')

            return render_template('index.html', form=form, titulo='Cadastrar')

    return render_template('index.html', form=form, titulo='Cadastrar')

@home_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.login'))

@home_bp.route('/teste')
@login_required
def teste():
    return 'O usuario atual é: '+current_user.nome