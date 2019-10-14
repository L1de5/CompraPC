# -*- coding: utf-8 -*-
__version__ = '0.1'
import os
from flask import Flask
from app.ext import database, login

app = Flask('app')
app.config.from_pyfile('../config.cfg')
database.configure(app)
login.configure(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

from app.controllers import *
