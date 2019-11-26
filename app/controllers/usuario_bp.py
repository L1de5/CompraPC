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

    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        senha = md5((form.senha.data).encode())
        conf_senha = md5((form.conf_senha.data).encode())
        endereco = form.endereco.data
        cpf = form.cpf.data
        data_nasc = form.data_nasc.data
        
        if senha.hexdigest() == conf_senha.hexdigest():
            novo_usuario = Usuario(nome = nome, email = email, senha = senha.hexdigest(), endereco = endereco, cpf = cpf, data_nasc = data_nasc)
            
            cadastro_usuario(novo_usuario)
            login_user(novo_usuario)
        else:
            flash(u'Ocorreu um problema ao tentar cadastrar usuário, as senhas não coincidem!', 'danger')

    return redirect('/produto')

@usuario_bp.route('/funcionario/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro_funcionario():
    if current_user.cargo == 'administrador':
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
    else:
        return redirect('/produto')

def cadastro_usuario(usuario):
    usuario_foi_cadastrado = Usuario.salvar(usuario)

    if usuario_foi_cadastrado:
        flash(u'Usuário cadastrado com sucesso!', 'success') 

        if Email.send_verificacao_email(usuario.email):
            flash(u'Email de verificação enviado com sucesso!', 'success') 
        else:  
            flash(u'Falha ao enviar email de verificação, tente novamente em outro momento!', 'danger')

    else: 
        flash(u'Ocorreu um problema ao tentar cadastrar usuário, tente novamente!', 'danger')

    return redirect('/produto')

@usuario_bp .route('/funcionario/listar', methods=['GET'])
@login_required
def listar():
    if current_user.cargo == 'administrador':
        funcionarios = Usuario.query.filter_by(cargo='funcionario')

        return render_template('buscas/funcionarios.html', funcionarios = funcionarios)
    else:
        flash(u'Você não tem permissão para acessar esta rota!', 'danger')

        return redirect('/produto')

@usuario_bp.route('/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario():
    form = EditarForm()

    form.nome.data = current_user.nome
    form.email.data = current_user.email
    form.endereco.data = current_user.endereco
    form.cpf.data = current_user.cpf
    form.data_nasc.data = current_user.data_nasc

    if request.method == 'POST':
        usuario = Usuario.query.get(current_user.id)
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        usuario.endereco = request.form['endereco']
        usuario.cpf = request.form['cpf']
        usuario.data_nasc = request.form['data_nasc']
        senha = request.form['senha']
        conf_senha = request.form['conf_senha']

        if senha.strip() and conf_senha.strip():
            senha_md5 = md5(senha.encode())
            conf_senha_md5 = md5(conf_senha.encode())

            if senha_md5.hexdigest() == conf_senha_md5.hexdigest():
                usuario.senha = senha_md5.hexdigest()
            else:
                flash(u'Ocorreu um problema ao tentar alterar funcionário, as senhas não coincidem!', 'danger')

        usuario_foi_salvo = Usuario.salvar(usuario)

        if usuario_foi_salvo:
            flash(u'Usuario alterado com sucesso!', 'success')

            return redirect('/produto')
        else:
            flash(
                u'Ocorreu um problema ao tentar alterar informacoes, tente novamente!', 'danger')

            return render_template('adicionarfuncionario.html', form=form, titulo='Editar')

    return render_template('adicionarfuncionario.html', form = form, titulo='Editar')

@usuario_bp.route('/editar/<id>', methods=['GET', 'POST'])
def editar_funcionario(id = False):
    form = EditarForm()
    usuario = Usuario.query.get(id)

    if current_user.cargo == 'administrador':
        if usuario:
            form.nome.data = usuario.nome
            form.email.data = usuario.email
            form.endereco.data = usuario.endereco
            form.cpf.data = usuario.cpf
            form.data_nasc.data = usuario.data_nasc

            if request.method == 'POST':
                usuario.nome = request.form['nome']
                usuario.email = request.form['email']
                usuario.endereco = request.form['endereco']
                usuario.cpf = request.form['cpf']
                usuario.data_nasc = request.form['data_nasc']
                senha = request.form['senha']
                conf_senha = request.form['conf_senha']

                if senha.strip() and conf_senha.strip():
                    senha_md5 = md5(senha.encode())
                    conf_senha_md5 = md5(conf_senha.encode())

                    if senha_md5.hexdigest() == conf_senha_md5.hexdigest():
                        usuario.senha = senha_md5.hexdigest()
                    else:
                        flash(u'Ocorreu um problema ao tentar alterar funcionário, as senhas não coincidem!', 'danger')

                usuario_foi_salvo = Usuario.salvar(usuario)

                if usuario_foi_salvo:
                    flash(u'Funcionário alterado com sucesso!', 'success')

                    return redirect('/produto')
                else:
                    flash(u'Ocorreu um problema ao tentar alterar informacoes, tente novamente!', 'danger')

                    return render_template('adicionarfuncionario.html', form=form, titulo='Editar')
        
        else:
            flash(u'Ocorreu um problema ao tentar buscar o usuário, tente novamente!', 'danger')

            return redirect('/funcionario/listar')

        return render_template('adicionarfuncionario.html', form = form, titulo='Editar')
    else:
        flash(u'Você não tem permissão para acessar esta rota!', 'danger')

        return redirect('/produto')

@usuario_bp.route('/deletarconta')
@login_required
def excluir_conta(id = False):
    id_usuario = current_user.id

    if Usuario.excluir(id_usuario):
        logout_user()
        flash(u'Sua conta foi excluida com sucesso!', 'success')
    else:
        flash(u'Falha ao excluir sua conta!', 'danger')
    
    return redirect('/produto')

@usuario_bp.route('/deletarconta/<id>')
@login_required
def excluir_conta_outro_user(id = False):
    if id and current_user.cargo == 'administrador':
        if Usuario.excluir(id):
            flash(u'A conta foi excluida com sucesso!', 'success')
        else:
            flash(u'Erro ao excluir conta!', 'danger')

        return redirect('/usuario/funcionario/listar')
    else:
        flash(u'Você não tem permissão para excluir contas de terceiros!', 'danger')
    
        return redirect('/produto')


@usuario_bp.route('/logout')
@login_required
def logout():
    logout_user()
    
    return redirect('/produto')
