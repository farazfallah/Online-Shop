
# Online Store Project (Python/Django)

## Description
This project is an **Online Store** built with Python and Django. It includes essential features for a shopping website, such as managing customers, products, orders, and categories. The platform is designed to be efficient, user-friendly, and scalable.

The frontend leverages **Bootstrap** for responsive design, providing a clean and professional user interface.

## Features
- **Customer Management**:
  - User registration and login (via OTP or username/password).
  - User profile and order history.
  - Logical deletion of inactive accounts.
- **Product Management**:
  - CRUD operations for products.
  - Support for product categories (tree structure).
  - Discounts and promo codes.
- **Order Management**:
  - Shopping cart with SPA design (using DRF).
  - Order finalization with discount application.
- **Admin Panel**:
  - Customized admin interface for ease of use.
  - Role-based access control (Product Manager, Supervisor, Operator).
- **Core Features**:
  - Base tools and utilities for cross-app functionality.
  - Multilingual support for broader accessibility.

## Technologies
- **Backend**:
  - Python/Django
  - PostgreSQL
  - Redis (for caching and OTP codes)
  - Celery (for task management)
- **Frontend**:
  - Bootstrap
  - HTML/CSS/JavaScript
- **Deployment**:
  - Docker/Docker Compose
  - Customized deployment using `Dockerfile`

## Project Structure
The project is divided into modular apps:
- **Customers**: Handles user information, authentication, and profiles.
- **Products**: Manages product details, discounts, and categories.
- **Orders**: Processes shopping carts and order histories.
- **Core**: Includes shared utilities and base models.

## Installation
Follow these steps to set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/your-repo-name.git
   ```
2. Set up a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configure the environment variables in a `.env` file (example provided in `.env.example`).
4. Start Docker services:
   ```bash
   docker-compose up --build
   ```
5. Run the migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

## Usage
1. Access the platform at `http://localhost:8000`.
2. Use the admin panel for management at `http://localhost:8000/admin`.

## Testing
- Unit tests cover a minimum of 80% of the code.
- Selenium tests for frontend functionality.
- Ensure comprehensive testing for robust performance.

## Deployment
1. Build the Docker image:
   ```bash
   docker build -t online-store .
   ```
2. Push the image to your Docker repository.
3. Use `docker-compose` for deployment:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Contributing
1. Fork the repository and clone your fork.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes and push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
4. Create a pull request from your branch to the main repository.
