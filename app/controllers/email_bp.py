# -*- coding: utf-8 -*-
from flask import *
from app.models.Email import Email
from app.models.banco.Usuario import Usuario
from flask_login import current_user, login_required

email_bp = Blueprint('email', __name__, url_prefix='/email')

@email_bp.route('/enviar/<valor>')
@login_required
def compra(valor): 
    email = current_user.email
    
    if Email.send_comprovante_compra(email, valor):
        flash(u'Comprovante enviado com sucesso!', 'success') 
    else:
        flash(u'Falha ao enviar comprovante, tente novamente!', 'danger')

    return redirect('/produto')

@email_bp.route('/enviarverificacao')
@login_required
def verificacao(): 
    if (current_user.email_verificado == 0):
        email = current_user.email

        if Email.send_verificacao_email(email):
            flash(u'Email de verificação enviado com sucesso!', 'success') 
        else:
            flash(u'Falha ao enviar email de verificação, tente novamente em outro momento!', 'danger')
    else: 
        flash(u'Email já foi verificado!', 'success')

    return redirect('/produto')

@email_bp.route('/confirmar/<token>')
@login_required
def confirm_email(token):
    if Email.verificar_email(token):
        email = current_user.email
        usuario = Usuario.query.filter_by(email = email).first()
        usuario.email_verificado = 1

        if Usuario.salvar(usuario):
            flash(u'Email verificado com sucesso!', 'success') 
        else:
            flash(u'Email não pode ser verificado, tente novamente em outro momento!', 'danger')
    else: 
        flash(u'Tempo de verificação expirado, tente novamente em outro momento!', 'danger')

    return redirect('/produto')
