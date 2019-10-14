from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, Length

class ProdutoForm(Form):
    nome = StringField('Nome', validators=[DataRequired(), Length(min = 3, max = 240)])
    descricao = StringField('Descrição', validators=[DataRequired(), Length(max = 400)])
    preco = IntegerField('Preço', validators=[DataRequired(), Length(min = 1, max = 80)])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), Length(min = 0, max = 240)])
    arquivo = FileField('Foto do Produto')
    submit = SubmitField('Cadastrar')
