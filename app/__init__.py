# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask
from app.ext import database, login

app = Flask('app')
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config.from_pyfile('../config.cfg')
database.configure(app)
login.configure(app)

from app.controllers import *
