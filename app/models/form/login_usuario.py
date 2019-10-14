from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(max = 320)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min = 3, max = 80)])
    submit = SubmitField('Entrar')