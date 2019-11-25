# -*- coding: utf-8 -*-
from app import app
from flask import *
from app.models.Email import Email
from app.models.banco.Usuario import Usuario
from app.models.form.login_usuario import LoginForm
from app.models.form.cadastro_usuario import CadastroForm
from app.models.form.editar_usuario import EditarForm
from flask_login import login_user, login_required, logout_user, current_user
from hashlib import md5

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
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
    form = CadastroForm()
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
    form = CadastroForm()

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
            return redirect("/produto")
        else:
            flash(u'Ocorreu um problema ao tentar cadastrar funcionário, as senhas não coincidem!', 'danger')

    return render_template('adicionarfuncionario.html', form=form, titulo='Adicionar Funcionario')

def cadastro_usuario(usuario):
    usuario_foi_cadastrado = Usuario.salvar(usuario)

    if usuario_foi_cadastrado:
        flash(u'Usuário cadastrado com sucesso!', 'success') 
        
        if usuario.cargo == "cliente":
            login_user(usuario)

        if Email.send_verificacao_email(usuario.email):
            flash(u'Email de verificação enviado com sucesso!', 'success') 
        else:  
            flash(u'Falha ao enviar email de verificação, tente novamente em outro momento!', 'danger')

    else: 
        flash(u'Ocorreu um problema ao tentar cadastrar usuário, tente novamente!', 'danger')

    return redirect('/produto')


@usuario_bp.route('/editar', methods=['GET', 'POST'])
@login_required
def editar():
    id = current_user.id
    cliente = Usuario.query.filter_by(id=id).first()

    if cliente:
        form_cliente = EditarForm()
        form_cliente.nome.data = cliente.nome
        form_cliente.email.data = cliente.email
        form_cliente.senha.data = cliente.senha
        form_cliente.endereco.data = cliente.endereco
        form_cliente.cpf.data = cliente.cpf
        form_cliente.data_nasc.data = cliente.data_nasc

        if request.method == 'POST':
            cliente = Usuario.query.filter_by(id=id).first()
            cliente.nome = request.form['nome']
            cliente.email = request.form['email']
            cliente.senha = request.form['senha']
            cliente.endereco = request.form['endereco']
            cliente.cpf = request.form['cpf']
            cliente.data_nasc = request.form['data_nasc']

            cliente_foi_salvo = Usuario.salvar(cliente)

            if cliente_foi_salvo:
                flash(u'Usuario alterado com sucesso!', 'success')

                return redirect('/produto')
            else:
                flash(
                    u'Ocorreu um problema ao tentar alterar informacoes, tente novamente!', 'danger')

                return render_template('adicionarfuncionario.html', form=form_cliente, titulo='Editar')

        return render_template('adicionarfuncionario.html', form = form_cliente, titulo='Editar')

@usuario_bp.route('/logout')
@login_required
def logout():
    logout_user()
    
    return redirect('/produto')
