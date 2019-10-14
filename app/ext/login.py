from flask_login import LoginManager
from app.models.banco.Cliente import Cliente
from flask import redirect

login_mananger = LoginManager()

def configure(app):
    login_mananger.init_app(app)
    app.login_mananger = login_mananger

@login_mananger.unauthorized_handler
def unauthorized():
    return redirect('/home')

@login_mananger.user_loader
def load_user(user_id):
    return Cliente.query.get(int(user_id))