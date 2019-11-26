from sqlalchemy import exc
from flask_sqlalchemy import SQLAlchemy
from app.ext.database import db
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from app.models.banco.ItemVenda import ItemVenda
from datetime import datetime

class Venda(db.Model): 
    __tablename__ = 'venda'

    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    comprador_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    item_venda_id = db.Column(db.Integer, db.ForeignKey('item_venda.id'))
