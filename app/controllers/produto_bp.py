# -*- coding: utf-8 -*-
from app import app
from flask import *
from app.models.form.cadastro_usuario import CadastroForm
from app.models.form.login_usuario import LoginForm
from app.models.form.produtos import ProdutoForm
from app.models.banco.Produto import Produto
from flask_login import login_required, current_user

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produto')

@produtos_bp.route('/')
def listar():
    form_cadastro = CadastroForm()
    form_login = LoginForm()
    produtos = Produto.query.order_by(Produto.id).all()

    return render_template('buscas/produtos.html', produtos = produtos, form_cadastro = form_cadastro, form_login = form_login)

@produtos_bp.route('/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar():
    form_produto = ProdutoForm()
    
    if form_produto.validate_on_submit():
        nome = form_produto.nome.data
        descricao = form_produto.descricao.data
        preco = form_produto.preco.data
        quantidade = form_produto.quantidade.data
        foto = form_produto.arquivo.data
        produto = Produto(nome = nome, descricao = descricao, preco = preco, quantidade = quantidade)

        produto_foi_salvo = Produto.salvar(produto, foto)

        if produto_foi_salvo:
            flash(u'Produto adicionado com sucesso!', 'success')

            return redirect('/produto')
        else:
            flash(u'Ocorreu um problema ao tentar adicionar produto, tente novamente!', 'danger')

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
        
        if request.method == 'POST':
            foto = form_produto.arquivo.data
            produto = Produto.query.filter_by(id=id).first()
            produto.nome = request.form['nome']
            produto.descricao = request.form['descricao']
            produto.preco = request.form['preco']
            produto.quantidade = request.form['quantidade']

            produto_foi_salvo = Produto.salvar(produto, foto)

            if produto_foi_salvo:
                flash(u'Produto alterado com sucesso!', 'success')

                return redirect('/produto')
            else:
                flash(u'Ocorreu um problema ao tentar alterar produto, tente novamente!', 'danger')

                return render_template('adicionarproduto.html', form_produto = form_produto, titulo='Produto')
        
        return render_template('adicionarproduto.html', form_produto = form_produto, titulo='Produto')

@produtos_bp.route('/detalhe/<id>', methods = ['GET', 'POST'])
def detalhe(id):
    form_cadastro = CadastroForm()
    form_login = LoginForm()
    produto = Produto.query.get(id)
    
    return render_template('buscas/detalhe_produto.html', produto = produto,  form_cadastro = form_cadastro, form_login = form_login)
 
@produtos_bp.route('/excluir/<id>', methods = ['GET', 'POST'])
@login_required
def excluir(id):
    produto = Produto.query.get(id)
    Produto.excluir(produto)

    return redirect('/produto/')