# -*- coding: utf-8 -*-
import os
from app import app
from flask import render_template, request, Blueprint, redirect, flash
from app.models.form.cadastro_usuario import CadastroForm
from app.models.form.login_usuario import LoginForm
from app.models.form.produtos import ProdutoForm
from app.models.banco.produto import Produto
from app.models.banco.Venda import Venda
from app.controllers.usuario_bp import *
from app.ext.login import *
from app.ext.database import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from hashlib import md5
from sqlalchemy import exc
from uuid import uuid4

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produto')

def permitido(extencao): 
    return extencao in ['png', 'jpg', 'jpeg']

@produtos_bp.route('/')
def listar():
    form_cadastro = CadastroForm()
    form_login = LoginForm()
    form_add_produto = ProdutoForm()
    produtos = Produto.query.order_by(Produto.id).all()

    return render_template('buscas/produtos.html', produtos = produtos, form_cadastro = form_cadastro, form_login = form_login, form_add_produto = form_add_produto)

@produtos_bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar():
    form_produto = ProdutoForm()
    print(form_produto.preco.data)
    
    if form_produto.validate_on_submit():
        nome = form_produto.nome.data
        descricao = form_produto.descricao.data
        preco = form_produto.preco.data
        quantidade = form_produto.quantidade.data
        arquivo = form_produto.arquivo.data
        extencao_foto = arquivo.filename.split('.')[-1].lower()
        novo_nome_foto = uuid4()
        is_permitido = permitido(extencao_foto)
         
        if is_permitido:
            novo_nome_foto = str(novo_nome_foto) + '.' + extencao_foto
            foto = secure_filename(arquivo.filename)
            diretorio = os.path.join(app.config['UPLOAD_FOLDER'], foto)
            diretorio_novo = os.path.join(app.config['UPLOAD_FOLDER'], novo_nome_foto)

            arquivo.save(diretorio)
            os.rename(diretorio, diretorio_novo)

            produto = Produto(nome = nome, descricao = descricao, preco = preco, quantidade = quantidade, arquivo = 'uploads/'+novo_nome_foto)

            try:
                db.session.add(produto)
                db.session.commit()
                flash(u'Produto adicionado com sucesso!', 'success')

                return redirect('/produto')
            except exc.SQLAlchemyError:
                flash(u'Ocorreu um problema ao tentar adicionar produto, tente novamente!', 'danger')

                return render_template('/produto')
        else:
            flash(u'Ocorreu um problema ao tentar adicionar produto, tente novamente!', 'danger')

            return render_template('adicionarproduto.html', form_produto = form_produto, titulo='Produto')

    return render_template('adicionarproduto.html', form_produto = form_produto, titulo='Produto')

@produtos_bp.route('/editar/<id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    produto = Produto.query.filter_by(id = id).first()

    if produto:
        form_produto = ProdutoForm()
        form_produto.nome.data = produto.nome
        form_produto.descricao.data = produto.descricao
        form_produto.preco.data = produto.preco
        form_produto.quantidade.data = produto.quantidade

        if form_produto.validate_on_submit():
            arquivo = form_produto.arquivo.data
            extencao_foto = arquivo.filename.split('.')[-1].lower()
            novo_nome_foto = uuid4()
            is_permitido = permitido(extencao_foto)
                
            if is_permitido:
                novo_nome_foto = str(novo_nome_foto) + '.' + extencao_foto
                foto = produto.arquivo.split('/')[-1]
                diretorio = os.path.join(app.config['UPLOAD_FOLDER'], foto)
                diretorio_novo = os.path.join(app.config['UPLOAD_FOLDER'], novo_nome_foto)
                os.remove(diretorio)
                arquivo.save(diretorio_novo)
                produto.arquivo = 'uploads/'+novo_nome_foto

            try:
                produto = Produto.query.filter_by(id = id).first()
                produto.nome = request.form['nome']
                produto.descricao = request.form['descricao']
                produto.preco = request.form['preco']
                produto.quantidade = request.form['quantidade']
                
                db.session.commit()

                flash(u'Produto alterado com sucesso!', 'success')

                return redirect('/produto')
            except exc.SQLAlchemyError:
                flash(u'Ocorreu um problema ao tentar alterar produto, tente novamente!', 'danger')

                return redirect('/produto/editar/' + id)

        return render_template('adicionarproduto.html', form_produto = form_produto, titulo='Produto')

@produtos_bp.route('/detalhe/<id>', methods = ['GET', 'POST'])
def detalhe(id):
    form_cadastro = CadastroForm()
    form_login = LoginForm()
    produto = Produto.query.get(id)
    
    return render_template('buscas/detalhe_produto.html', produto=produto,  form_cadastro = form_cadastro, form_login = form_login)

@produtos_bp.route('/carrinho')
def carrinho():
    cliente = current_user
    produtos = cliente.prod_cart

    return render_template('buscas/carrinho.html', produtos = produtos)


@produtos_bp.route('/addC/<id>', methods = ['GET', 'POST'])
@login_required
def addCart(id):
    cliente = current_user
    produto = Produto.query.get(id)
    cliente.prod_cart.append(produto)
    db.session.merge(cliente)
    db.session.commit()
    return redirect('/produto')
 
@produtos_bp.route('/excluir/<id>', methods = ['GET', 'POST'])
@login_required
def excluir(id):
    try:
        produto = Produto.query.get(id)
        foto = produto.arquivo.split('/')[-1]
        diretorio = os.path.join(app.config['UPLOAD_FOLDER'], foto)
        os.remove(diretorio)
        db.session.delete(produto)
        db.session.commit()
        
        flash(u'Produto deletado com sucesso!', 'success')
    except exc.SQLAlchemyError:
        flash(u'Ocorreu um problema ao tentar deletar produto, tente novamente!', 'danger')

    return redirect('/produto/')


