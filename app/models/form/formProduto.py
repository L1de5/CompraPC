from flask_wtf import Form, csrf
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms_components import EmailField
from wtforms.widgets import TextArea



class Produtos(Form):
    id = IntegerField('id')
    nome = StringField('nome')
    descricao = StringField('descricao', widget=TextArea())
    preco = IntegerField('preco')
    quantidade = IntegerField('quantidade')
    submit = SubmitField('enviar')
