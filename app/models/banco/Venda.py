from flask_sqlalchemy import SQLAlchemy
from app import db

class Venda(db.Model): 
    __tablename__ = 'venda'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    comprador = db.Column(db.Integer, nullable=False)
