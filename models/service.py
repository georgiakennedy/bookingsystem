from init import db, ma

class Service(db.Model):
    """
    Model representing a service offered.

    This class defines the structure of the 'services' table in the database,
    which holds information about each service available.

    Attributes:
        service_id (int): Primary key for the service record.
        service_type (str): Type of the service (must not be null).
        price (float): Price of the service (must not be null).
    """
    __tablename__ = "services"

    service_id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class ServiceSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for serializing and deserializing Service instances.

    This class defines how Service instances are converted to and from
    JSON format for API responses and requests.

    Meta:
        model (Service): The model to be serialized.
    """
    class Meta:
        model = Service

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)