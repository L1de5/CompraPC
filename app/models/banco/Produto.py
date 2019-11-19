from flask_sqlalchemy import SQLAlchemy
from app.ext.database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

class Produto(db.Model):
    __tablename__ = 'produto'

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    descricao = db.Column(db.String(200), nullable = False)
    preco = db.Column(db.Float, nullable = False)
    quantidade = db.Column(db.Integer, nullable = False)
    arquivo = db.Column(db.String(400), nullable = False)
  
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            