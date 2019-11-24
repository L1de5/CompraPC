# -*- coding: utf-8 -*-
import os
from app import app
from flask import *
from app.models.banco.Produto import Produto
from app.models.CarrinhoCompras import CarrinhoCompras
from flask_login import login_required, current_user

carrinho_compras_bp = Blueprint('carrinho', __name__, url_prefix='/carrinho')
carrinho = CarrinhoCompras()

@carrinho_compras_bp.route('/')
@login_required
def listar_itens():
    carrinho.set_itens_from_session()
    itens = carrinho.get_itens()

    return render_template('buscas/carrinho.html', itens = itens)

@carrinho_compras_bp.route('/adicioanaritem/<id>', methods = ['GET'])
@login_required
def adicionar_item(id):
    carrinho.set_itens_from_session()
    produto_dict = Produto.get_dict_produto(id)
    dict_item = {}
    dict_item['produto'] = produto_dict
    dict_item['quantidade'] = 1

    if carrinho.adicionar_item(dict_item):
        flash(u'Produto adicionado ao carrinho com sucesso!', 'success')
    else:
        flash(u'Limite do estoque deste produto atingido!', 'danger')

    return redirect('/produto')
 
@carrinho_compras_bp.route('/excluiritem/<id>', methods = ['GET', 'POST'])
@login_required
def excluir(id):
    produto_dict = Produto.get_dict_produto(id)
    carrinho.remover_item(produto_dict)
    flash(u'Produto removido do carrinho com sucesso!', 'success')

    return redirect('/produto')


