# -*- coding: utf-8 -*-
from flask_mail import Mail, Message
from app.ext.mail import serialize_obj, mail
from flask import Blueprint, request, url_for
from flask_login import current_user, login_required
from app.models.banco.Cliente import Cliente
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

email_bp = Blueprint('email', __name__, url_prefix='/email')

# Exemplo de virificação de email

@email_bp.route('/enviar')
@login_required
def cadastro(): 
    email = current_user.email
    token = serialize_obj.dumps(email, salt='email-confirm')
    message = Message(
        'Confirm Email', sender='jp.20011973@gmail.com', recipients=[email])
    link = url_for('email.confirm_email', token = token, _external = True)
    message.body = 'Por favor verifique sua conta clicando no link: {}'.format(link)

    try:
        mail.send(message)
    except Exception:
        return 'Não foi possivel enviar email de verificação, tente novamente em outro momento!'

    return 'The email is: {} and the tokes is: {}'.format(current_user.email, token)

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
