from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize extensions for the Flask application

db = SQLAlchemy()  # SQLAlchemy instance for database management and ORM functionality
ma = Marshmallow()  # Marshmallow instance for object serialization and deserialization
bcrypt = Bcrypt()  # Bcrypt instance for hashing passwords securely
jwt = JWTManager()  # JWTManager instance for handling JSON Web Tokens for authentication
