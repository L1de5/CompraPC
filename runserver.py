import os
import app
from flask import Blueprint, Flask
from flask import redirect, url_for, render_template
from app.controllers.home_bp import home_bp
from app import db
import flask_sqlalchemy
import os
 
app = Flask(__name__, template_folder='.')
app.register_blueprint(home_bp)
uri= "postgresql://postgres:postgres@localhost:5432/dbteste"
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db.init_app(app)
@app.route("/")
def index():
    return redirect("/home")
 
if __name__ == '__main__':
    app.run(debug=True, port=5000)




