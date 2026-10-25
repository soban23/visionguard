import os
from flask import Flask
from .models import db

def create_app(database_uri=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri or os.environ.get(
        "DATABASE_URL", "sqlite:///visionguard.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
