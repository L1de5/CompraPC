# -*- coding: utf-8 -*-
import os
from app import app
from flask import render_template, request, Blueprint, redirect, flash
from app.models.form.cadastro_usuario import CadastroForm
from app.models.form.login_usuario import LoginForm
from app.models.form.produtos import ProdutoForm
from app.models.banco.produto import Produto
from app.models.banco.Venda import Venda
from app.ext.database import db
from flask_login import login_required
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
    produtos = Produto.query.all()

    return render_template('buscas/listarp.html', produtos = produtos, form_cadastro = form_cadastro, form_login = form_login, form_add_produto = form_add_produto)

@produtos_bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar():
    form_produto = ProdutoForm()
    
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

    return render_template('quests/produtos.html', form_produto = form_produto, titulo='Produto')

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
                foto = secure_filename(arquivo.filename)
                diretorio = os.path.join(app.config['UPLOAD_FOLDER'], foto)
                diretorio_novo = os.path.join(app.config['UPLOAD_FOLDER'], novo_nome_foto)
                arquivo.save(diretorio)
                os.rename(diretorio, diretorio_novo)
                produto.arquivo = novo_nome_foto

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

                return render_template('/produto/editar' + id)

        return render_template('quests/produtos.html', form_produto = form_produto, titulo='Produto')

@produtos_bp.route('/detalhe/<id>', methods = ['GET', 'POST'])
@login_required
def detalhe(id):
    produto = Produto.query.get(id)
    
    return render_template('buscas/detalhe.html', produto=produto)

 
@produtos_bp.route('/excluir/<id>', methods = ['GET', 'POST'])
@login_required
def excluir(id):
    try:
        produto = Produto.query.get(id)
        db.session.delete(produto)
        db.session.commit()
        flash(u'Produto deletado com sucesso!', 'success')
    except exc.SQLAlchemyError:
        flash(u'Ocorreu um problema ao tentar deletar produto, tente novamente!', 'danger')

    return redirect('/produto/')


