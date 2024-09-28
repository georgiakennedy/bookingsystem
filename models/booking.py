from init import db, ma

class Booking(db.Model):
    """
    Model representing a booking for a service.

    This class defines the structure of the 'bookings' table in the database,
    which holds information about each booking made by users.

    Attributes:
        booking_id (int): Primary key for the booking record.
        user_id (int): Foreign key reference to the user making the booking (must not be null).
        date_id (int): Foreign key reference to the available date for the booking (must not be null).
        service_id (int): Foreign key reference to the service being booked (must not be null).
        employee_id (int): Foreign key reference to the employee assigned to the booking (must not be null).
        dog_breed (str): Breed of the dog for the booking (optional).
        dog_weight (float): Weight of the dog for the booking (optional).
    """
    __tablename__ = "bookings"

    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_id = db.Column(db.Integer, db.ForeignKey('available_dates.date_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    dog_breed = db.Column(db.String(100))
    dog_weight = db.Column(db.Float)

class BookingSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for serializing and deserializing Booking instances.

    This class defines how Booking instances are converted to and from
    JSON format for API responses and requests.

    Meta:
        model (Booking): The model to be serialized.
    """
    class Meta:
        model = Booking

booking_schema = BookingSchema()
bookings_schema = BookingSchema(many=True)