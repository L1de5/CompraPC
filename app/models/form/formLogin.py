from flask_wtf import Form, csrf
from wtforms import StringField, SubmitField, IntegerField, FloatField, PasswordField, DateField
from wtforms_components import EmailField

class Login(Form):
    email = StringField('email')
    senha = PasswordField('senha')
    submit = SubmitField('enviar')
