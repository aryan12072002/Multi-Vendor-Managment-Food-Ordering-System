
# Food Ordering System

## Introduction
Welcome to the **Food Ordering System** project! This web application allows users to browse, order, and manage their food from various restaurants. The system provides a seamless experience for both restaurant owners and customers. Restaurant owners can manage their menus, while customers can easily browse, order, and track their food deliveries.

## Features
- **User Account Management**: Customers can create accounts, log in, and manage their profiles.
- **Restaurant Menus**: Browse different restaurants and their menus with easy access to food items.
- **Order Placement**: Add items to your cart, place orders, and track the status of your order.
- **Admin Panel**: Restaurant owners can manage their menus, add, update, and delete items.
- **Secure Payment System**: Integrated payment gateway for secure transactions.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Python, Django
- **Database**: MySQL
- **Payment Gateway**: Razorpay (or other services)

## Installation Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AryanTayade/food-ordering-system.git
   ```

2. **Install the required dependencies:**
   ```bash
   cd food-ordering-system
   pip install -r requirements.txt
   ```

3. **Configure MySQL Database:**
   - Create a database in MySQL and update the `DATABASES` settings in the `settings.py` file with your database credentials.

4. **Migrate the Database:**
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application:**
   Open your browser and navigate to `http://127.0.0.1:8000/` to start using the Food Ordering System.

## Project Structure
```
food-ordering-system/
├── assets/                # Static files (images, CSS, JavaScript)
├── food_ordering/         # Main Django app for managing orders and restaurants
├── manage.py              # Django's command-line utility
├── requirements.txt       # List of dependencies
└── food_ordering_system/  # Django project folder
    ├── settings.py        # Django settings
    ├── urls.py            # URL configurations
    └── wsgi.py            # WSGI entry point
```

## Contributing
We welcome contributions to this project! If you'd like to contribute, please fork the repository, create a new branch, and submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or feedback, feel free to reach out to **Aryan Tayade**.

---

Thank you for checking out the **Food Ordering System**! We hope it provides a seamless and enjoyable experience for users and restaurant owners alike.
