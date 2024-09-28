from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.employee import Employee
from models.service import Service
from models.available_date import AvailableDate

# Create a Blueprint for database management commands
db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    """
    Create all database tables.

    This command initializes the database by creating all tables
    defined in the models. It should be run once to set up the database.

    Returns:
        None
    """
    db.create_all()  # Create all tables based on the models defined
    print("Tables created.")  # Print confirmation message

@db_commands.cli.command("seed")
def seed_tables():
    """
    Seed the database with initial data.

    This command populates the database with predefined user, employee,
    and service instances. It is useful for testing and development.

    Returns:
        None
    """
    # Create a list of user instances
    users = [
        User(
            name="Admin",
            email="admin@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),  # Hash the password for security
            mobile_number=1234567890,  # Use an integer for mobile number
            is_admin=True  # Mark this user as an admin
        ),
        User(
            name="User A",
            email="usera@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),  # Hash the password for security
            mobile_number=9876543210  # Use an integer for mobile number
        )
    ]
    
    # Create a list of employee instances
    employees = [
        Employee(
            name="Employee1"  # Create an employee with the specified name
        ),
        Employee(
            name="Employee2"  # Create another employee with the specified name
        )
    ]

    # Create a list of service instances
    services = [
        Service(
            service_type="Basic Grooming",  # Define the type of service
            price=50.00  # Set the price for the service
        ),
        Service(
            service_type="Deluxe Grooming",  # Define another type of service
            price=75.00  # Set the price for this service
        )
    ]

    # Add all user instances to the database session
    db.session.add_all(users)  # Add the list of users to the session
    db.session.add_all(employees)  # Add the list of employees to the session
    db.session.add_all(services)  # Add the list of services to the session
    # db.session.add_all(available_dates)  # Uncomment to add available dates if defined
    
    db.session.commit()  # Commit the session to save all changes to the database
    print("Tables seeded.")  # Print confirmation message

@db_commands.cli.command("drop")
def drop_tables():
    """
    Drop all database tables.

    This command removes all tables from the database. Use with caution
    as all data will be lost.

    Returns:
        None
    """
    db.drop_all()  # Drop all tables from the database
    print("Tables dropped.")  # Print confirmation message