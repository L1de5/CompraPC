# -*- coding: utf-8 -*-
import os
from app import app
from flask import render_template, request, Blueprint, redirect, flash, session, jsonify
from app.models.banco.Produto import Produto
from flask_login import login_required, current_user
from sqlalchemy import exc

carrinho_compras_bp = Blueprint('carrinho', __name__, url_prefix='/carrinho')

@carrinho_compras_bp.route('/', methods=['GET', 'POST'])
@login_required
def carrinho():
    cliente = current_user
    produtos = cliente.prod_cart

    return render_template('buscas/carrinho.html', produtos = produtos)


@carrinho_compras_bp.route('/adicioanarproduto/<id>', methods = ['GET', 'POST'])
@login_required
def adicionar_produto(id):
    cliente = current_user
    produto = Produto.query.get(id)

    if produto in cliente.prod_cart:
        flash(u'Produto já se encontra no carrinho!', 'danger')
    else:
        if (produto.quantidade > 0):
            cliente.prod_cart.append(produto)
            db.session.merge(cliente)
            db.session.commit()

            flash(u'Produto adicionado ao carrinho com sucesso!', 'success')
        else:
            flash(u'Produto não esta mais em estoque', 'danger')

    return redirect('/produto/')
 
@carrinho_compras_bp.route('/excluir/<id>', methods = ['GET', 'POST'])
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


