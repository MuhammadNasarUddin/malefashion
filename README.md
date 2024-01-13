[Watch the Video](https://www.youtube.com/watch?v=malefashion.mp4)
# Male Fashion Ecommerce Django Project

Welcome to the Male Fashion Ecommerce Django project! This project is designed to provide a dynamic and user-friendly platform for selling male fashion products. Users can explore various categories, apply filters, add products to their cart, and proceed to checkout. The project also supports user authentication, allowing users to log in via email or Google.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Authentication](#authentication)

## Features
- Dynamic display of categories and products
- Search and filter functionality
- User authentication via email and Google
- Shopping cart management
- Email notification on checkout

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/MuhammadNasarUddin/malefashion.git
    cd malefashion
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Apply migrations:
    ```bash
    python manage.py migrate
    ```

6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage
1. Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.
2. Explore the available categories and products.
3. Use the search and filter options to find specific products.
4. Add products to your cart.
5. Log in before proceeding to checkout.
6. Receive an email notification upon successful checkout.

## Authentication
### Email Authentication
- Users can create an account using their email address and password.
- Passwords are securely stored using Django's authentication system.

### Google Authentication
- Users can log in using their Google account.
- Configure your Google API credentials in the Django admin for authentication.


