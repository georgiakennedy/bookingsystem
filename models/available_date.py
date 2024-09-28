from init import db, ma

class AvailableDate(db.Model):
    """
    Model representing an available date for booking.

    This class defines the structure of the 'available_dates' table in the
    database, including attributes that describe the date, time, and booking status.

    Attributes:
        date_id (int): Primary key for the available date record.
        date (date): The date for which the booking is available.
        time (time): The specific time for the available booking.
        is_booked (bool): Indicates if the date and time are booked (default is False).
        user_id (int): Foreign key reference to the user who booked the date (nullable).
    """
    __tablename__ = "available_dates"

    date_id = db.Column(db.Integer, primary_key=True)  # Primary key
    date = db.Column(db.Date, nullable=False)            # Date of the booking
    time = db.Column(db.Time, nullable=False)            # Time of the booking
    is_booked = db.Column(db.Boolean, default=False)     # Booking status
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)  # Reference to the user

    user = db.relationship('User', backref='available_dates')  # Relationship with User

class AvailableDateSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for serializing and deserializing AvailableDate instances.

    This class defines how AvailableDate instances are converted to and from
    JSON format and includes options for serialization.

    Meta:
        model (AvailableDate): The model to be serialized.
        include_fk (bool): Whether to include foreign key fields in the serialized output.
    """
    class Meta:
        model = AvailableDate
        include_fk = True  # Include foreign keys in serialization

available_date_schema = AvailableDateSchema()  # Single instance schema
available_dates_schema = AvailableDateSchema(many=True)  # List of instances schema