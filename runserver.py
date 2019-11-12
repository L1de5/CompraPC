#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from app import app
from flask_bootstrap import Bootstrap
from flask import redirect, Blueprint
from app.controllers.setup_bp import setup_bp
from app.controllers.usuario_bp import usuario_bp
from app.controllers.produto_bp import produtos_bp
from app.controllers.email_bp import email_bp
from app.ext.database import db

app.register_blueprint(setup_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(produtos_bp)
app.register_blueprint(email_bp)

@app.route('/')
def index():
    return redirect(produtos_bp.url_prefix)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8180))
    bootstrap = Bootstrap(app)
    
    app.run('0.0.0.0', port=port)
