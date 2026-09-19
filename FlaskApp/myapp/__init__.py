# myapp/__init__.py

from flask import Flask
from sqlalchemy import event
from sqlalchemy.engine import Engine
from config import Config
from myapp.extensions import db, login_manager, migrate


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if dbapi_connection.__class__.__module__.startswith("sqlite3"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    from myapp import models    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    
    # Register blueprints
    from myapp.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    from myapp.boards.routes import boards_bp
    app.register_blueprint(boards_bp)
    from myapp.home.routes import home_bp
    app.register_blueprint(home_bp)
    from myapp.people.routes import people_bp
    app.register_blueprint(people_bp)
    from myapp.assignments.routes import assignments_bp
    app.register_blueprint(assignments_bp)

    return app
