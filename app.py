import os
from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.cli_controllers import db_commands
from controllers.auth_controller import auth_bp
from controllers.main_controllers import main_bp  # Import the main controller

def create_app():
    """
    Create and configure the Flask application.

    This function initializes the Flask application, sets up the necessary
    configurations, and registers the required blueprints for the application.

    Returns:
        app (Flask): The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")  # Set your database URL
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")  # Set your JWT secret key

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)  # Register the main controller

    return app