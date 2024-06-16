# Django Friend Request API

This project is a Django-based REST API for managing friend requests. It uses Django Rest Framework (DRF) and JWT for authentication. The project is containerized using Docker and Docker Compose.

# Features

    1. User Registration and Login with JWT Authentication
    2. Sending Friend Requests
    3. Accepting/Rejecting Friend Requests
    4. Viewing Friends List
    5. Searching Users by Email or Name
    6. Rate-limiting on sending friend requests

# Installation

## Prerequisites

Make sure you have the following installed on your machine:

    Python 3.10
    pip (Python package installer)
    virtualenv (optional but recommended for creating an isolated Python environment)

## Setup Instructions

    1.  Clone the Repository

    git clone https://github.com/yourusername/django-friend-request-api.git

    cd django-friend-request-api

    2. Create and Activate a Virtual Environment

    python3 -m venv venv
    source venv/bin/activate  

    3. Install the Required Packages

    pip install -r requirements.txt

    4. Apply Migrations

    Run the following command to apply the database migrations:

    python manage.py migrate

    5. Run the Development Server

    python manage.py runserver

    The application will be available at http://localhost:8000.

# Usage
## Register a New User

Send a POST request to `/api/v1/register/` with the following payload:

    {
        "username": "yourusername",
        "password": "yourpassword",
        "email": "youremail@example.com"
    }

## Login
Send a POST request to `/api/v1/login/` with the following payload:

    {
        "username": "yourusername",
        "password": "yourpassword"
    }

The response will include a JWT token which you will use to authenticate further requests.

## Friend Requests

### Send a Friend Request

Send a POST request to `/api/v1/friend-request/` with the following payload, including the JWT token in the Authorization header:

    {
        "request_to": 2  # The ID of the user to whom the friend request is being sent
    }


### View Friend Requests

Send a GET request to `/api/v1/friend-request/` including the JWT token in the Authorization header. This will return all received and sent friend requests.

### Accept a Friend Request

Send a PUT request to `/api/v1/friend-request/<id>/` including the JWT token in the Authorization header, where <id> is the ID of the friend request.

### Delete a Friend Request

Send a DELETE request to `/api/v1/friend-request/<id>/` including the JWT token in the Authorization header, where <id> is the ID of the friend request. Accepted requests cannot be deleted.

### Friends List

Send a GET request to `/api/v1/friends/` including the JWT token in the Authorization header. This will return the list of friends for the authenticated user.

### Search Users

Send a GET request to `/api/v1/search/` including the JWT token in the Authorization header with a query parameter for the search keyword.

    To search by email: /api/v1/search/?query=email@example.com
    To search by name: /api/v1/search/?query=John

