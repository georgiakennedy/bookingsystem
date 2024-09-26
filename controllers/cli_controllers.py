from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.employee import Employee

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created.")

@db_commands.cli.command("seed")
def seed_tables():
    # create a list of user instances
    users = [
        User(
            name="Admin",
            email="admin@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
            mobile_number=1234567890,  # Use an integer for mobile number
            is_admin=True
        ),
        User(
            name="User A",
            email="usera@email.com",
            password=bcrypt.generate_password_hash("123456").decode("utf-8"),
            mobile_number=9876543210  # Use an integer for mobile number
        )
    ]

    employee = [
        Employee(
            name = "Employee1"
        ),
        Employee(
            name = "Employee2"
        )
    ]


    db.session.add_all(users)
    db.session.add_all(employee)
    db.session.commit()
    print("Tables seeded.")


@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped.")