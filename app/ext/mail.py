from app import app
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

mail = Mail(app)
serialize_obj = URLSafeTimedSerializer('Thisisasecret')