from flask_wtf import Form, csrf
from wtforms import StringField, SubmitField, IntegerField, FloatField, PasswordField, DateField
from wtforms_components import EmailField

class Clientes(Form):
    id = IntegerField('id')
    nome = StringField('nome')
    email = StringField('email')
    senha = PasswordField('senha')
    endereco = StringField('endereco')
    cpf = StringField('cpf')
    dataNasc = DateField('dataNasc', format='%DD/%MM/%YY')
    submit = SubmitField('enviar')
