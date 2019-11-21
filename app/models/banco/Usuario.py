from sqlalchemy import *
from sqlalchemy import exc
from app.ext.database import db
from flask_login import UserMixin
from app.models.banco.Venda import Venda
from sqlalchemy.orm import relationship, backref

class Usuario(UserMixin, db.Model): 
    __tablename__= 'usuario'

    id = db.Column(db.Integer, autoincrement = True ,primary_key = True)
    nome = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    senha = db.Column(db.String(100), nullable = False)
    endereco = db.Column(db.String(100), nullable = False)
    cpf = db.Column(db.String(11), nullable = False, unique = True)
    data_nasc = db.Column(db.Date, nullable = False)
    email_verificado = db.Column(db.Integer, nullable = False, default = 0)
    cargo = db.Column(db.String(100), default = 'cliente')
    comprador_vendas = db.relationship('Venda', backref='comprador', lazy='select')


    @staticmethod
    def salvar(usuario):
        try:
            db.session.add(usuario)
            db.session.commit()

            return redirect('/email/enviarverificacao')
        except exc.SQLAlchemyError:
            flash(u'Ocorreu um problema ao tentar cadastrar funcionário, tente novamente!', 'danger')
        
        return redirect('/produto')
