from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    username = StringField('Email', validators=[DataRequired(), Length(max = 320)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min = 3, max = 80)])
    submit = SubmitField('Entrar')