from sqlalchemy import exc
from datetime import datetime
from app.ext.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.banco.Produto import Produto

class ItemVenda(db.Model): 
    __tablename__ = 'item_venda'

    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    preco = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Integer, nullable = False, default = 1)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
    vendas_item = db.relationship('Venda', backref='item_venda', lazy='select')

    @staticmethod
    def item_to_dict(produto, quantidade):
        dict_item_venda = {}
        dict_produto = Produto.to_dict(produto)
        dict_item_venda['produto'] = dict_produto
        dict_item_venda['quantidade'] = quantidade

        return dict_item_venda
