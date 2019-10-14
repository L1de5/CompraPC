# -*- coding: utf-8 -*-
from flask import render_template, request, Blueprint, redirect, url_for, flash
from app.models.form.cadastro_usuario import CadastroForm
from app.models.form.login_usuario import LoginForm
from app.models.form.produtos import ProdutoForm
from app.models.banco.Cliente import Cliente
from app.models.banco.produto import Produto
from app.models.banco.Venda import Venda
from app.ext.database import db
from app.ext.login import login_mananger
from flask_login import login_user, login_required, logout_user, current_user
from hashlib import md5
from sqlalchemy import exc

home_bp = Blueprint('home', __name__, url_prefix='/home')

@home_bp.route('/', methods=['GET', 'POST'])
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

                return redirect('/home/produto')
            else:
                flash(u'Senha inválida!', 'danger')
        else:
            flash(u'Usuário inválido!', 'danger')

    return render_template('index.html', form = form, titulo = 'Logar')

@home_bp.route('/cadastro', methods=['GET', 'POST'])
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

            return redirect('/home/')
        except exc.SQLAlchemyError:
            flash(u'Ocorreu um problema ao tentar cadastrar usuário, tente novamente!', 'danger')

            return render_template('index.html', form=form, titulo='Cadastrar')

    return render_template('index.html', form=form, titulo='Cadastrar')

@home_bp.route('/produto', methods=['GET', 'POST'])
def produto():
    form = ProdutoForm()

    if request.method == "POST":
        nome = form.nome.data
        descricao = form.descricao.data
        preco = form.preco.data
        quantidade = form.quantidade.data
        produto = Produto(nome = nome, descricao = descricao, preco = preco, quantidade = quantidade)

        try:
            db.session.add(produto)
            db.session.commit()
            #login_usuario(new_user) Explica ai

            return redirect('/home/')
        except exc.SQLAlchemyError:
            flash(u'Ocorreu um problema ao tentar cadastrar usuário, tente novamente!', 'danger')

            return render_template('index.html', form=form, titulo='Cadastrar')

    return render_template('index.html', form=form, titulo='Produto')

@home_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.login'))

@home_bp.route('/teste')
@login_required
def teste():
    return 'O usuario atual é: '+current_user.nome