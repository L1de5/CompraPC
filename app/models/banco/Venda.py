from flask_sqlalchemy import SQLAlchemy
from app.ext.database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.models.banco.Usuario import Usuario
from app.models.banco.Produto import Produto

class Venda(db.Model): 
    __tablename__ = 'venda'

    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.DateTime, nullable = False)
    comprador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
