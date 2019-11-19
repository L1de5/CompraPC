from flask import redirect
from flask_login import LoginManager
from app.models.banco.Usuario import Usuario

login_mananger = LoginManager()

def configure(app):
    login_mananger.init_app(app)
    app.login_mananger = login_mananger

    @login_mananger.unauthorized_handler
    def unauthorized():
        return redirect('/produto')

    @login_mananger.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))