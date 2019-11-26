import json
from sqlalchemy import *
from sqlalchemy import exc
from app.ext.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from flask import redirect, flash
from app.models.Foto import Foto

class Produto(db.Model):
    __tablename__ = 'produto'

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    descricao = db.Column(db.String(200), nullable = False)
    preco = db.Column(db.Float, nullable = False)
    quantidade = db.Column(db.Integer, nullable = False)
    arquivo = db.Column(db.String(400), nullable = False)
    item_vendas = db.relationship('ItemVenda', backref='produto', lazy='select')
  
    @staticmethod
    def buscar(palavra):
        try:
            if palavra:
                palavra = '%{}%'.format(palavra)
                produtos = Produto.query.filter(Produto.nome.ilike(palavra)).order_by(Produto.id).all()
            else:
                produtos = Produto.query.order_by(Produto.id).all()

            return produtos
        except exc.SQLAlchemyError:
            return False


    @staticmethod
    def salvar(produto, foto = None):
        try:
            if foto:
                nome_foto = Foto.salvar(foto)

                if nome_foto:
                    produto.arquivo = 'uploads/' + nome_foto

            if produto.id:
                db.session.merge(produto)

            else:
                db.session.add(produto)

            db.session.commit()

            return True
        except exc.SQLAlchemyError:
            return False

    @staticmethod
    def excluir(produto):
        try:
            foto_removida = Foto.excluir(produto.arquivo)
            print(foto_removida)
        
            if foto_removida:
                db.session.delete(produto)
                db.session.commit()
                
                flash(u'Produto deletado com sucesso!', 'success')
            else:
                flash(u'Ocorreu um problema ao tentar deletar produto, tente novamente!', 'danger')

        except exc.SQLAlchemyError:
            flash(u'Ocorreu um problema ao tentar deletar produto, tente novamente!', 'danger')

        return redirect('/produto/')
            
    @staticmethod
    def get_dict_produto(id):
        produto = Produto.query.get(id)

        return produto.to_dict()

    def to_dict(self):
        dictionary = self.__dict__
        dictionary.pop('_sa_instance_state')

        return dictionary
