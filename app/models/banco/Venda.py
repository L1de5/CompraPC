from flask_sqlalchemy import SQLAlchemy
from app.ext.database import db

venda_produto = db.Table('venda_produto', db.Column('id_venda', db.Integer, db.ForeignKey(
    'venda.id'), primary_key=True), db.Column('id_produto', db.Integer, db.ForeignKey('produto.id'), primary_key=True))


class Venda(db.Model): 
    __tablename__ = 'venda'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    comprador = db.Column(db.Integer, nullable=False)
    prod_venda = db.relationship('Produto', secondary=venda_produto, backref='venda')
