from app.ext.database import db
from flask_login import UserMixin
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float

carrinho = db.Table('carrinho', db.Column('id_cliente',db.Integer, db.ForeignKey('cliente.id'), primary_key=True),db.Column('id_produto', db.Integer, db.ForeignKey('produto.id'), primary_key=True))

class Cliente(UserMixin, db.Model): 
    __tablename__= 'cliente'
    id = db.Column(db.Integer, autoincrement = True ,primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    data_nasc = db.Column(db.Date, nullable=False)
    prod_cart = db.relationship('Produto', secondary=carrinho, backref='cliente')
