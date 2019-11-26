# -*- coding: utf-8 -*-
import os
from app import app
from flask import *
from app.models.banco.Produto import Produto
from app.models.CarrinhoCompras import CarrinhoCompras
from app.models.banco.Venda import Venda
from app.models.banco.ItemVenda import ItemVenda
from flask_login import login_required, current_user
from datetime import datetime
from app.ext.database import db

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
    
    if carrinho.remover_item(produto_dict):
        flash(u'Produto removido do carrinho com sucesso!', 'success')
    else:
        flash(u'O produto não se encontra no carrinho!', 'danger')

    return redirect('/produto')

@carrinho_compras_bp.route('/alterarquantidade', methods = ['GET', 'POST'])
@login_required
def alterar_quantidade():
    if request.method == 'POST':
        indice_item = int(request.values.get('indice'))
        quantidade_nova = int(request.values.get('quantidade_nova'))
        carrinho.alterar_quantidade_item(indice_item, quantidade_nova)

    return redirect('/')


@carrinho_compras_bp.route('/comprar', methods=['GET', 'POST'])
@login_required
def comprar():
    valor_total = carrinho.get_valor_total()
    item = carrinho.get_itens()
    venda = Venda()
    item_venda = ItemVenda()
    for item in item:
        produto = Produto.query.get(item['produto']['id'])
        produto.quantidade = produto.quantidade - item['quantidade']
        Produto.salvar(produto)
        item_venda.data = datetime.now()
        item_venda.preco = item['produto']['preco']
        item_venda.quantidade = item['quantidade']
        item_venda.produto_id = item['produto']['id']
        db.session.add(item_venda)
        db.session.commit()
        venda.data = datetime.now()
        venda.comprador_id = current_user.id
        venda.item_venda_id = item_venda.id
        db.session.add(venda)
        db.session.commit()
    carrinho.limpar()
    return render_template("/buscas/compra.html", valor=valor_total)
