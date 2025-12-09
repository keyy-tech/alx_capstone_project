Perfect! Based on your `SPECTACULAR_SETTINGS` and the context from your project (Django, DRF, Djoser, multi-restaurant app), here’s a professional **README.md** draft you can use and expand as needed:

````markdown
# Multi Restaurant API

**Version:** 1.0.0  

**Author:** Emmanuel Kotoka  
**Email:** emmanuelyayrakotoka@gmail.com  

## Overview
Multi Restaurant API is a Django-based backend application that allows users to register, authenticate, and interact with multiple restaurants. Think of it like Bolt Food but with support for multiple restaurants. It features user registration, profiles, authentication, and a structured API for restaurant operations.

## Features
- User registration and login (Customer & Owner roles)
- User profiles with additional details
- JWT authentication via Djoser
- Restaurant management (CRUD operations)
- Support for multiple restaurants
- RESTful API endpoints with DRF
- Swagger/OpenAPI documentation via drf-spectacular

## Tech Stack
- Python 3.11+
- Django 4.x
- Django REST Framework
- Djoser (for authentication)
- drf-spectacular (for API schema & documentation)
- SQLite / PostgreSQL (configurable)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/multi-restaurant-api.git
cd multi-restaurant-api
````

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows use: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

## API Documentation

Once the server is running, you can access the API documentation at:

```
http://127.0.0.1:8000/api/schema/   # OpenAPI schema
http://127.0.0.1:8000/api/docs/     # Swagger UI
```

## Endpoints

* `POST /api/v1/register/customer/` - Register a customer
* `POST /api/v1/register/owner/` - Register a restaurant owner
* `POST /api/v1/token/` - Obtain JWT token
* `POST /api/v1/token/refresh/` - Refresh JWT token
* `GET /api/v1/users/me/` - Retrieve current user info

*(Add more endpoints as you implement restaurant and order functionality)*

## Running Tests

```bash
python manage.py test
```

## Contribution

Feel free to fork the repository, open issues, or submit pull requests. Please follow PEP8 style guidelines.

