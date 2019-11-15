from app.ext.database import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref

class Usuario(UserMixin, db.Model): 
    __tablename__= 'usuario'

    id = db.Column(db.Integer, autoincrement = True ,primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    senha = db.Column(db.String(100), nullable = False)
    endereco = db.Column(db.String(100), nullable = False)
    cpf = db.Column(db.String(11), nullable = False)
    data_nasc = db.Column(db.Date, nullable = False)
    email_verificado = db.Column(db.Integer, nullable = False, default = 0)
    cargo = db.Column(db.String(100), default = 'cliente')
    comprador = db.relationship('Usuario', backref = 'comprador', cascade = 'all, delete')
