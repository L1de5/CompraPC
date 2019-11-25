from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length

class EditarForm(Form):
    nome = StringField('Nome', validators=[DataRequired(), Length(min = 3, max = 240)])
    email = StringField('Email', validators=[DataRequired(), Email(message = 'Email inválido'), Length(max = 320)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min = 3, max = 80)])
    endereco = StringField('Endereço', validators=[DataRequired(), Length(min = 3, max = 240)])
    cpf = StringField('CPF', validators=[DataRequired(), Length(min = 11, max = 11)])
    data_nasc = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Salvar')
