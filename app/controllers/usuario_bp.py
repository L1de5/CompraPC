# -*- coding: utf-8 -*-
from app import app
from flask import *
from app.models.banco.Usuario import Usuario
from app.models.form.login_usuario import LoginForm
from app.models.form.cadastro_usuario import CadastroForm
from flask_login import login_user, login_required, logout_user
from hashlib import md5
from app.ext.database import db
from sqlalchemy import exc

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    db.create_all()
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        senha = md5(form.senha.data.encode())
        usuario = Usuario.query.filter_by(email = email).first()

        if usuario:
            if usuario.senha == senha.hexdigest():
                login_user(usuario)
            else:
                flash(u'Senha inválida!', 'danger')
        else:
            flash(u'Usuário inválido!', 'danger')

    return redirect('/produto')

@usuario_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = md5((request.form['senha']).encode())
        conf_senha = md5((request.form['conf_senha']).encode())
        endereco = request.form['endereco']
        cpf = request.form['cpf']
        data_nasc = request.form['data_nasc']
        
        if senha.hexdigest() == conf_senha.hexdigest():
            novo_usuario = Usuario(nome = nome, email = email, senha = senha.hexdigest(), endereco = endereco, cpf = cpf, data_nasc = data_nasc)
            
            cadastro_usuario(novo_usuario)
        else:
            flash(u'Ocorreu um problema ao tentar cadastrar usuário, as senhas não coincidem!', 'danger')

    return redirect('/produto')

@usuario_bp.route('/funcionario/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro_funcionario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = md5((request.form['senha']).encode())
        conf_senha = md5((request.form['conf_senha']).encode())
        endereco = request.form['endereco']
        cpf = request.form['cpf']
        data_nasc = request.form['data_nasc']
        cargo = 'funcionario'
        
        if senha.hexdigest() == conf_senha.hexdigest():
            novo_usuario = Usuario(nome = nome, email = email, senha = senha.hexdigest(), endereco = endereco, cpf = cpf, data_nasc = data_nasc, cargo = cargo)
            
            cadastro_usuario(novo_usuario)
        else:
            flash(u'Ocorreu um problema ao tentar cadastrar funcionário, as senhas não coincidem!', 'danger')

    return redirect('/produto')

def cadastro_usuario(usuario):
    Usuario.salvar(usuario)
    login_user(usuario)

@usuario_bp.route('/logout')
@login_required
def logout():
    logout_user()
    
    return redirect('/produto')
