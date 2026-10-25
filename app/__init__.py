import os
from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/visionguard")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
