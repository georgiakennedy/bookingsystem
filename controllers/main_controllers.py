from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta 
from models.user import User, user_schema, users_schema
from models.booking import Booking, booking_schema, bookings_schema
from models.available_date import AvailableDate, available_date_schema, available_dates_schema
from models.employee import Employee, employee_schema, employees_schema
from models.service import Service, service_schema, services_schema
from init import db

# Create a Blueprint for the main application
main_bp = Blueprint("main", __name__)

# User routes
@main_bp.route('/users', methods=['GET'])
def get_users():
    """
    Retrieve all users from the database.

    This endpoint responds to GET requests and returns a list of all
    users in JSON format. The users are serialized using the users_schema.

    Returns:
        JSON response containing a list of users.
    """
    users = users_schema.dump(User.query.all())  # Query all User records from the database
    return jsonify(users)  # Return the serialized list of users

@main_bp.route('/users', methods=['POST'])
def add_user():
    """
    Add a new user to the database.

    This endpoint responds to POST requests and expects JSON data
    containing user details. It creates a new User instance and 
    saves it to the database after adding it to the session. 

    Request Body:
        - username: The desired username for the new user.
        - email: The user's email address.
        - password: The user's password (should be hashed before saving).
        - phone_number: The user's phone number.

    Returns:
        JSON response containing the newly created user.
        HTTP status code 201 if successful.
    """
    new_user = User(
        username=request.json['username'],
        email=request.json['email'],
        password=request.json['password'],  # Hash this before saving
        phone_number=request.json['phone_number']
    )
    db.session.add(new_user)  # Add the new user to the database session
    db.session.commit()  # Commit the session to save the new user
    return user_schema.dump(new_user), 201  # Return the serialized user data with a 201 status

# Booking routes
@main_bp.route('/bookings', methods=['GET'])
def get_bookings():
    """
    Retrieve all bookings from the database.

    This endpoint responds to GET requests and returns a list of all
    bookings in JSON format. The bookings are serialized using the bookings_schema.

    Returns:
        JSON response containing a list of bookings.
    """
    bookings = bookings_schema.dump(Booking.query.all())  # Query all Booking records from the database
    return jsonify(bookings)  # Return the serialized list of bookings

@main_bp.route('/bookings', methods=['POST'])
def add_booking():
    """
    Create a new booking.

    This endpoint responds to POST requests and expects JSON data containing
    booking details. It validates the requested time against existing bookings
    and creates a new Booking instance if valid.

    Request Body:
        - user_id: The ID of the user making the booking.
        - date: The date for the booking (YYYY-MM-DD format).
        - time: The time for the booking (HH:MM:SS format).
        - service_id: The ID of the service being booked.
        - employee_id: The ID of the employee assigned to the booking.
        - dog_breed: The breed of the dog for the booking.
        - dog_weight: The weight of the dog for the booking.

    Returns:
        JSON response containing the newly created booking.
        HTTP status code 201 if successful, or error messages if validation fails.
    """
    # Extract information from the request
    user_id = request.json['user_id']
    date = request.json['date']  # Expecting a full date string
    time = request.json['time']   # Expecting a time string

    # Convert string time to datetime object
    booking_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    end_time = booking_time + timedelta(hours=1)  # End time is one hour later

    # Check for overlapping bookings
    overlapping_booking = AvailableDate.query.filter(
        AvailableDate.date == date,
        AvailableDate.is_booked == True,
        (AvailableDate.time >= booking_time.time()) &
        (AvailableDate.time < end_time.time())
    ).first()  # Fetch first overlapping booking if exists

    if overlapping_booking:
        return jsonify({"error": "The selected time is already booked."}), 400  # Return error if time is booked

    # Check for last booking that ends within one hour before the requested time
    last_booking_check = AvailableDate.query.filter(
        AvailableDate.date == date,
        AvailableDate.is_booked == True,
        (AvailableDate.time + timedelta(hours=1) > booking_time.time())  # Last booking overlaps with requested time
    ).first()  # Fetch first last booking if exists

    if last_booking_check:
        return jsonify({"error": "The selected time is less than one hour after the last booking."}), 400  # Return error if too close to last booking

    # If no overlapping booking exists, create or update the available date
    available_date = AvailableDate.query.filter_by(date=date, time=booking_time.time()).first()  # Check if available date exists

    if not available_date:
        # If it doesn't exist, create a new available date
        available_date = AvailableDate(
            date=date,
            time=booking_time.time(),
            is_booked=True,
            user_id=user_id  # Set the user_id
        )
        db.session.add(available_date)  # Add the new available date to the session
        db.session.commit()  # Commit to get the available_date.date_id for the booking
    else:
        # If it exists and is not booked, just update the user_id
        available_date.is_booked = True  # Mark as booked
        available_date.user_id = user_id  # Update user_id
        db.session.commit()  # Commit the changes

    # Create the new booking
    new_booking = Booking(
        user_id=user_id,
        date_id=available_date.date_id,  # Use date_id here
        service_id=request.json['service_id'],
        employee_id=request.json['employee_id'],
        dog_breed=request.json['dog_breed'],
        dog_weight=request.json['dog_weight']
    )

    db.session.add(new_booking)  # Add the new booking to the session
    db.session.commit()  # Commit to save the new booking

    return booking_schema.dump(new_booking), 201  # Return the serialized booking data with a 201 status

# Available Dates routes
@main_bp.route('/available_dates', methods=['GET'])
def get_available_dates():
    """
    Retrieve all available dates from the database.

    This endpoint responds to GET requests and returns a list of all
    available dates in JSON format. The dates are serialized using the available_dates_schema.

    Returns:
        JSON response containing a list of available dates.
    """
    dates = available_dates_schema.dump(AvailableDate.query.all())  # Query all AvailableDate records from the database
    return jsonify(dates)  # Return the serialized list of available dates

@main_bp.route('/available_dates', methods=['POST'])
def add_available_date():
    """
    Add a new available date to the database.

    This endpoint responds to POST requests and expects JSON data
    containing available date details. It creates a new AvailableDate
    instance and saves it to the database.

    Request Body:
        - date: The date for the available slot (YYYY-MM-DD format).
        - time: The time for the available slot (HH:MM:SS format).
        - is_booked: A boolean indicating if the slot is booked (default is False).

    Returns:
        JSON response containing the newly created available date.
        HTTP status code 201 if successful.
    """
    new_date = AvailableDate(
        date=request.json['date'],
        time=request.json['time'],
        is_booked=request.json.get('is_booked', False)
    )
    db.session.add(new_date)  # Add the new available date to the session
    db.session.commit()  # Commit the session to save the new available date
    return available_date_schema.dump(new_date), 201  # Return the serialized available date with a 201 status

# Employee routes
@main_bp.route('/employees', methods=['GET'])
def get_employees():
    """
    Retrieve all employees from the database.

    This endpoint responds to GET requests and returns a list of all
    employees in JSON format. The employees are serialized using the employees_schema.

    Returns:
        JSON response containing a list of employees.
    """
    employees = employees_schema.dump(Employee.query.all())  # Query all Employee records from the database
    return jsonify(employees)  # Return the serialized list of employees

@main_bp.route('/employees', methods=['POST'])
def add_employee():
    """
    Add a new employee to the database.

    This endpoint responds to POST requests and expects JSON data
    containing employee details. It creates a new Employee instance 
    and saves it to the database.

    Request Body:
        - name: The name of the employee.

    Returns:
        JSON response containing the newly created employee.
        HTTP status code 201 if successful.
    """
    new_employee = Employee(
        name=request.json['name']
    )
    db.session.add(new_employee)  # Add the new employee to the session
    db.session.commit()  # Commit the session to save the new employee
    return employee_schema.dump(new_employee), 201  # Return the serialized employee data with a 201 status

# Service routes
@main_bp.route('/services', methods=['GET'])
def get_services():
    """
    Retrieve all services from the database.

    This endpoint responds to GET requests and returns a list of all
    services in JSON format. The services are serialized using the services_schema.

    Returns:
        JSON response containing a list of services.
    """
    services = services_schema.dump(Service.query.all())  # Query all Service records from the database
    return jsonify(services)  # Return the serialized list of services

@main_bp.route('/services', methods=['POST'])
def add_service():
    """
    Add a new service to the database.

    This endpoint responds to POST requests and expects JSON data
    containing service details. It creates a new Service instance 
    and saves it to the database.

    Request Body:
        - service_type: The type of service being offered.
        - price: The price of the service.

    Returns:
        JSON response containing the newly created service.
        HTTP status code 201 if successful.
    """
    new_service = Service(
        service_type=request.json['service_type'],
        price=request.json['price']
    )
    db.session.add(new_service)  # Add the new service to the session
    db.session.commit()  # Commit the session to save the new service
    return service_schema.dump(new_service), 201  # Return the serialized service data with a 201 status