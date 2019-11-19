# -*- coding: utf-8 -*-
from flask_mail import Mail, Message
from app.ext.mail import serialize_obj, mail
from flask import Blueprint, request, url_for, redirect, flash
from flask_login import current_user, login_required
from app.models.banco.Usuario import Usuario
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

email_bp = Blueprint('email', __name__, url_prefix='/email')

@email_bp.route('/enviar/<valor>')
@login_required
def compra(valor): 
    email = current_user.email
    message = Message('Compravante de compra', sender='digaomartins8@gmail.com', recipients=[email])
    message.body = 'Sua compra no valor de R$ '+ valor +' foi realizada com sucesso!'

    try:
        mail.send(message)
        flash(u'Comprovante enviado com sucesso!', 'success') 
    except Exception:
        flash(u'Falha ao enviar comprovante, tente novamente!', 'danger')

    return redirect('/produto')

@email_bp.route('/enviarverificacao')
@login_required
def verificacao(): 
    email = current_user.email
    token = serialize_obj.dumps(email, salt='email-confirm')
    message = Message('Compra PC', sender='digaomartins8@gmail.com', recipients=[email])
    link = url_for('email.confirm_email', token = token, _external = True)
    message.body = 'Verifique seu eail clicando no link: '+link

    try:
        mail.send(message)
        flash(u'Email de verificação enviado com sucesso!', 'success') 
    except Exception:
        flash(u'Falha ao enviar email de verificação, tente novamente!', 'danger')

    return redirect('/produto')

@email_bp.route('/confirmar/<token>')
@login_required
def confirm_email(token):
    try:
        email = current_user.email
        user = Cliente.query.filter_by(email = email).first()
        email = serialize_obj.loads(token, salt='email-confirm', max_age = 3600)
    except SignatureExpired:
        return '<h1> Email verificado com sucesso </h1>'

    return '<h1> Email não pode ser verificado, tente novamente em outro momento! </h1>'
