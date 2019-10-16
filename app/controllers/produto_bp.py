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
def produto():
    form = ProdutoForm()

    if request.method == "POST":
        nome = form.nome.data
        descricao = form.descricao.data
        preco = form.preco.data
        quantidade = form.quantidade.data
        arquivo = form.arquivo.data
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

                return redirect('/produto')
            except exc.SQLAlchemyError:
                flash(u'Ocorreu um problema ao tentar adicionar produto, tente novamente!', 'danger')

                return render_template('/produto')
        else:
            flash(u'Ocorreu um problema ao tentar adicionar produto, tente novamente!', 'danger')

    return render_template('index.html', form=form, titulo='Produto')

@produtos_bp.route('/detalhe/<id>', methods = ['GET', 'POST'])
@login_required
def detalhe(id):
    produto = Produto.query.get(id)
    
    return render_template('buscas/detalhe.html', produto=produto)

 
@produtos_bp.route('/excluir/<id>', methods = ['GET', 'POST'])
@login_required
def excluir(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect('/produto/')


