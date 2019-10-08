# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect
from app.models.banco.funcionario import Funcionario
from app.models.banco.cliente import Cliente
from app.models.banco.produto import Produto
from app.models.banco.venda import Venda
from app.models.form.formProduto import Produtos
from app.models.form.formLogin import Login
from app.models.form.formCliente import Clientes
from app import db
home_bp = Blueprint('home', __name__, url_prefix='/home')


@home_bp.route('/')
def home():
    db.create_all()
    return redirect('/home/login')

@home_bp.route('/produtos', methods=['GET', 'POST'])
def projeto():
    form=Produtos()
    if request.method == 'POST':
        ids = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        if ids == '':
            p = Produto(nome=nome, descricao=descricao, preco=preco, quantidade=quantidade)
            db.session.add(p)
        else:
            p = Produto(id=ids, nome=nome, descricao=descricao, preco=preco, quantidade=quantidade)
            db.session.merge(p)
        db.session.commit()
        return render_template('app/templates/quests/index.html')
    return render_template('app/templates/quests/produtos.html', form=form)

@home_bp.route('/clientes', methods=['GET', 'POST'])
def clientes():
    form=Clientes()
    if request.method == 'POST':
        ids = request.form['id']
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        endereco = request.form['endereco']
        cpf = request.form['cpf']
        dataNasc = request.form['dataNasc']
        if ids == '':
            c = Cliente(nome=nome, email=email,senha=senha, endereco=endereco, cpf=cpf, dataNasc=dataNasc)
            db.session.add(c)
        else:
            c = Cliente(id=ids, nome=nome,email=email,senha=senha, endereco=endereco, cpf=cpf, dataNasc=dataNasc)
            db.session.merge(c)
        db.session.commit()
        return render_template('app/templates/quests/index.html')
    return render_template('app/templates/quests/cadastro.html', form=form)

@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    form=Login()
    if request.method == 'POST':
        email=request.form['email']
        senha=request.form['senha']
        l = Cliente.query.filter_by(email=email)
        if senha == l[0].senha:
            return render_template('app/templates/quests/index.html')
    return render_template('app/templates/quests/login.html', form=form)



@home_bp.route('/listarP')
def listarP():
    lista = Produto.query.all()
    return render_template('app/templates/buscas/listarp.html', func=lista)

@home_bp.route('/listarC')
def listarC():
    lista = Cliente.query.all()
    return render_template('app/templates/buscas/listarC.html', func=lista)

