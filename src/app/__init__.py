import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

flask_app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = "announcements.db"




flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, DB_NAME)}"
flask_app.config["DEBUG"] = True
flask_app.config["CSRF_ENABLED"] = True
flask_app.config["CSRF_SESSION_KEY"] = "secret"
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
flask_app.config["SECRET_KEY"] = "secret"

db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)

from app.views import announcements_bp, hosts_bp

flask_app.register_blueprint(announcements_bp)
flask_app.register_blueprint(hosts_bp)
