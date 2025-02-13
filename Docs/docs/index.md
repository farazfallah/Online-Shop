# Online Store Project

## Project Overview  
This project is an **e-commerce website** built with **Django**. It includes various sections such as customer management, product management, order processing, and more. The main goal of this project is to develop a fully functional online store with features like inventory management, discounts, authentication, and a shopping cart system.

### Technologies Used  
- **Backend**: Django, Django REST Framework, Celery, Docker  
- **Database**: PostgreSQL, Redis (for caching and OTP verification)  
- **Frontend**: HTML, CSS, JavaScript, Bootstrap, Tailwind CSS, jQuery  

### Features  
- **Customer Management**: User registration, login (via OTP or password), profile management  
- **Product Management**: Categories, discounts, and stock control  
- **Order Processing**: Shopping cart, order history, and checkout  
- **Admin Panel**: Custom Django Admin with role-based access control  
- **Security & Deployment**: JWT authentication, soft delete for data safety, and Docker-based deployment  

## Project Structure  
The project is divided into modular apps:

- **Customers**: Handles user information, authentication, and profiles.  
- **Products**: Manages product details, discounts, and categories.  
- **Orders**: Processes shopping carts and order histories.  
- **Core**: Includes shared utilities and base models.  

## Setup & Deployment  

### Installation  
Follow these steps to set up the project locally:

1. Clone the repository:
   ```sh
   git clone https://github.com/YourUsername/your-repo-name.git
   ```
2. Set up a virtual environment and install dependencies:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configure the environment variables in a `.env` file (example provided in `.env.example`).
4. Start Docker services:
   ```sh
   docker-compose up --build
   ```
5. Run the migrations:
   ```sh
   python manage.py migrate
   ```
6. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```

### Usage  
- Access the platform at: [http://localhost:8000](http://localhost:8000)
- Use the admin panel for management at: [http://localhost:8000/admin](http://localhost:8000/admin)

### Testing  
- Unit tests cover a minimum of 80% of the code.  
- Selenium tests for frontend functionality.  
- Ensure comprehensive testing for robust performance.  

### Deployment  
1. Build the Docker image:
   ```sh
   docker build -t online-store .
   ```
2. Push the image to your Docker repository.  
3. Use `docker-compose` for deployment:
   ```sh
   docker-compose -f docker-compose.prod.yml up -d
   ```

## Contributing  
1. Fork the repository and clone your fork.  
2. Create a new branch:
   ```sh
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes and push to your fork:
   ```sh
   git push origin feature/your-feature-name
   ```
4. Create a pull request from your branch to the main repository.  

## API Endpoints  
This section outlines the available API endpoints for the project.

### Authentication APIs  
- `POST /api/login/password/` - Login using a password.  
- `POST /api/login/otp/request/` - Request an OTP for authentication.  
- `POST /api/login/otp/` - Login using an OTP.  
- `POST /api/register/` - Register a new user.  
- `POST /api/validate-token/` - Validate authentication token.  
- `POST /api/logout/` - Logout from the system.  

### User & Profile APIs  
- `GET /api/profile/` - Retrieve user profile information.  

### Product APIs  
- `GET /api/categories/` - Retrieve product categories.  
- `GET /api/products/` - List all products.  
- `GET /api/products/{id}/` - Get product details.  
- `GET /api/product-images/` - Retrieve product images.  
- `GET /api/product-comments/` - Retrieve comments on products.  
- `POST /api/products/{id}/comments/` - Add a comment to a product.  

### Address APIs  
- `GET /api/addresses/` - Retrieve user addresses.  
- `POST /api/addresses/add/` - Add a new address.  
- `PUT /api/addresses/edit/{address_id}/` - Edit an existing address.  
- `DELETE /api/addresses/delete/{address_id}/` - Delete an address.  

### Order & Cart APIs  
- `GET /api/cart/` - Retrieve the shopping cart.  
- `POST /api/checkout/` - Proceed to checkout.  
- `GET /api/orders/` - List user orders.  
- `GET /api/orders/{order_id}/` - Retrieve order details.  
- `POST /api/verify-discount/` - Verify a discount code.  

### Site Information API  
- `GET /api/site-info/` - Retrieve site-wide information.  

All product-related endpoints are registered under `/api/` through Django's `DefaultRouter`.