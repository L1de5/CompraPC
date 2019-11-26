from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from wtforms.fields.html5 import IntegerField

class EditarProdutoForm(Form):
    style = {
        'type' : 'number',
        'step' : '0.01'
    }
    
    nome = StringField('Nome', validators=[DataRequired(), Length(min = 3, max = 240)])
    descricao = TextAreaField('Descrição', validators=[DataRequired(), Length(max = 400)])
    preco = DecimalField('Preço',  validators=[DataRequired(), NumberRange(min = 0)],render_kw=style)
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min = 0)])
    arquivo = FileField('Foto do Produto')
    submit = SubmitField('Adicionar')
