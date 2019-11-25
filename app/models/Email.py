# -*- coding: utf-8 -*-
from flask import current_app, url_for
from flask_mail import Mail, Message
from app.ext.mail import serialize_obj, mail
from app.models.banco.Usuario import Usuario
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

class Email(): 

    @staticmethod
    def send_comprovante_compra(email, valor):
        message = Message('Compravante de compra', sender = current_app.config['MAIL_USERNAME'], recipients=[email])
        message.body = 'Sua compra no valor de R$ '+ valor +' foi realizada com sucesso!'

        return Email.email_sender(message)

    @staticmethod
    def send_verificacao_email(email):
        token = serialize_obj.dumps(email, salt = 'email-confirm')
        message = Message('Compra PC', sender = current_app.config['MAIL_USERNAME'], recipients=[email])
        link = url_for('email.confirm_email', token = token, _external = True)
        message.body = 'Verifique seu email <a href="{}"> clicando aqui. </a>'.format(link)
        
        return Email.email_sender(message)

    @staticmethod
    def verificar_email(token):
        try:
            email = serialize_obj.loads(token, salt='email-confirm', max_age = 86400)

            return True
        except SignatureExpired:
            return False

    @staticmethod
    def email_sender(message):
        try:
            mail.send(message)

            return True
        except Exception:
            return False
