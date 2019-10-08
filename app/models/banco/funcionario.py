from flask_sqlalchemy import SQLAlchemy
from app import db

class Funcionario(db.Model): 
    __tablename__= 'funcionario'
    id = db.Column(db.Integer, autoincrement = True ,primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    dataNasc = db.Column(db.Date, nullable=False)
