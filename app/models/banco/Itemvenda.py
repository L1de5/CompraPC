from datetime import datetime
from app.ext.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.models.banco.Usuario import Usuario
from app.models.banco.Produto import Produto

class Itemvenda(db.Model): 
    __tablename__ = 'item_venda'

    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    quantidade = db.Column(db.Integer, nullable = False, default = 1)
    comprador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
