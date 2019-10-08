from flask_sqlalchemy import SQLAlchemy
from app.models.banco.venda import Venda
from app import db

venda_produto = db.Table('venda_produto', db.Column('id_venda',db.Integer, db.ForeignKey('venda.id'), primary_key=True),db.Column('id_produto', db.Integer, db.ForeignKey('produto.id'), primary_key=True))

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    vendas = db.relationship('Venda', secondary=venda_produto, backref='produto')


