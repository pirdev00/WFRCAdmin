# myapp/__init__.py

from flask import Flask
from config import Config
from myapp.extensions import db, login_manager, migrate

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

    return app