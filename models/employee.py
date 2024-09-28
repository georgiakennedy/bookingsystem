from init import db, ma

class Employee(db.Model):
    """
    Model representing an employee.

    This class defines the structure of the 'employees' table in the database,
    which holds information about each employee.

    Attributes:
        employee_id (int): Primary key for the employee record.
        name (str): Name of the employee (must not be null).
    """
    __tablename__ = "employees"

    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema for serializing and deserializing Employee instances.

    This class defines how Employee instances are converted to and from
    JSON format for API responses and requests.

    Meta:
        model (Employee): The model to be serialized.
    """
    class Meta:
        model = Employee

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


