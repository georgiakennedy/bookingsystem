from flask import Blueprint, request
from models.user import User, user_schema
from init import bcrypt, db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():
    """
    Register a new user.

    This endpoint responds to POST requests and expects JSON data
    containing user details. It creates a new User instance, hashes
    the password, and saves it to the database.

    Request Body:
        - name: The name of the user.
        - email: The user's email address (must be unique).
        - mobile_number: The user's mobile number (must be unique).
        - password: The user's password.

    Returns:
        JSON response containing the newly created user data.
        HTTP status code 201 if successful, or error messages if validation fails.
    """
    try:
        # get the data from the body of the request
        body_data = request.get_json()
        # create an instance of the user model
        user = User(
            name=body_data.get("name"),
            email=body_data.get("email"),
            mobile_number=body_data.get("mobile_number")
        )
        # hash the password
        password = body_data.get("password")
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        
        # add and commit to the DB
        db.session.add(user)
        db.session.commit()
        
        # return acknowledgment
        return user_schema.dump(user), 201
    except IntegrityError as err:
        # Check for NOT NULL violation
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"{err.orig.diag.column_name} is required."}, 400
        
        # Check for UNIQUE violation
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            column_name = getattr(err.orig.diag, 'column_name', None)
            if column_name:
                if "mobile_number" in column_name:
                    return {"error": "Mobile number is already in use."}, 400
                elif "email" in column_name:
                    return {"error": "Email address is already in use."}, 400
                
        # Handle unexpected errors
        return {"error": "An unexpected error occurred."}, 500


@auth_bp.route("/login", methods=["POST"])
def login_user():
    """
    Log in an existing user.

    This endpoint responds to POST requests and expects JSON data
    containing login credentials. It checks the user's email and 
    password, and if valid, generates a JWT for authenticated access.

    Request Body:
        - email: The user's email address.
        - password: The user's password.

    Returns:
        JSON response containing the user's email, admin status, and the JWT token.
        HTTP status code 200 if successful, or an error message if login fails.
    """
    # Get the data from the body of the request
    body_data = request.get_json()
    # Find the user in DB with that email address
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    # If user exists and pw is correct
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        # create JWT
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        # Respond back
        return {"email": user.email, "is_admin": user.is_admin, "token": token}
    # Else
    else:
        # Respond back with an error message
        return {"error": "Incorrect email or password"}, 400