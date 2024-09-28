from init import db, ma

class User(db.Model):
    """
    Model representing a user in the system.

    This class defines the structure of the 'users' table in the database,
    which holds information about each user.

    Attributes:
        user_id (int): Primary key for the user record.
        name (str): Name of the user (optional).
        password (str): Password for the user account (must not be null).
        email (str): Email address of the user (must not be null, must be unique).
        mobile_number (int): Mobile number of the user (must not be null, must be unique).
        is_admin (bool): Indicates if the user has admin privileges (default is False).
    """
    __tablename__ = "users"

    #attributes of the table
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    mobile_number = db.Column(db.BigInteger, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.Schema):
    """
    Schema for serializing and deserializing User instances.

    This class defines how User instances are converted to and from
    JSON format for API responses and requests.

    Meta:
        fields (tuple): Fields to be included in the serialized output.
    """
    class Meta:
        fields = ("id", "name", "password", "email", "mobile_number", "is_admin")

#to handle a single user object
user_schema = UserSchema(exclude=["password"])

#to handle a list of user objects
users_schema = UserSchema(many=True, exclude=["password"])