# Project README

## Table of Contents

- Project Overview
- Features
- Technologies Used
- API Endpoints
- Database Models
- How to Run the Project

## Project Overview

This application is designed to manage dog grooming bookings. It provides a platform for users to register, set their availability, book services, and manage their pets' details. The backend is built using Python with SQLAlchemy for ORM, and it exposes a RESTful API for client interactions.

## Features

- User registration and authentication
- Manage available dates for grooming services
- Book a grooming service for pets
- View all available services and employees
- Retrieve user-specific bookings

## Technologies Used

- **Backend**: Python, Flask
- **Database**: PostgreSQL (or SQLite for development)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger/OpenAPI

## API Endpoints

Below is a list of available API endpoints:

### User Endpoints

- **Register User**: `POST /auth/register`
- **Login User**: `POST /auth/login`

### Available Dates Endpoints

- **Create Available Date**: `POST /available_dates`

### Booking Endpoints

- **Book a Date**: `POST /bookings`
- **Get All Bookings for User**: `GET /bookings`

### Service Endpoints

- **Get All Services**: `GET /services`

### Employee Endpoints

- **Get All Employees**: `GET /employees`

## Database Models

The application consists of several models representing the database structure:

1. **User**: Represents users of the application (attributes: user_id, name, password, email, mobile_number, is_admin).
2. **AvailableDate**: Represents dates and times available for booking services (attributes: date_id, date, time, is_booked, user_id).
3. **Booking**: Represents a booking (attributes: booking_id, user_id, date_id, service_id, employee_id, dog_breed, dog_weight).
4. **Service**: Represents the grooming services available (attributes: service_id, service_type, price).
5. **Employee**: Represents employees managing bookings (attributes: employee_id, name).

## How to Run the Project

1. **Clone the Repository**:
bash
git clone https: //github.com/yourusername/your-repo.git
cd your-repo

2. **Set Up a Virtual Environment**:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install Dependencies**:
pip install -r requirements.txt

4. **Set Up the Database**:
Update your dataase configuration in the config.py file.
Initialise the database:
flask db init
flask db migrate
flask fb upgrade

5. **Run the application**:
flask run

6. **Acess the API**:
Access the API on a browser or API program such as Insomnia.
