# Flask E-commerce Application

This application is a simple e-commerce platform built using Flask and SQLAlchemy. It allows users to browse and purchase various products, manage a shopping cart, place orders with delivery details, and view past orders. The app uses SQLite for data storage and handles cart management via Flask sessions. Admins can view and manage all orders placed by customers.

## Key Features

- **Product Catalog**: Displays different categories of products (vegetables, fruits, dairy, beverages, and meal boxes) to choose from.
- **Shopping Cart**: Users can add items to their cart, update quantities, and remove items.
- **Order Placement**: Users can provide delivery details and place orders. The total cost includes product prices and shipping charges.
- **Admin Dashboard**: Admins can view all orders placed by customers, including detailed information about each order.
- **Session Management**: The cart is maintained in the user's session, ensuring items persist until the user checks out or clears their cart.
- **User Registration**: Users can register and store their details for future orders (authentication is basic at this stage).

## Technologies Used

- **Flask**: Web framework used to build the application.
- **SQLAlchemy**: ORM for managing the database (SQLite in this case).
- **SQLite**: Lightweight database used for storing product, order, and delivery information.
- **Jinja2**: Templating engine used for rendering HTML pages.
- **Flask Flash Messages**: Provides feedback to users on actions such as successful order placement or errors like mismatched passwords.

## Conclusion

This Flask e-commerce app offers a basic yet functional shopping experience, allowing users to browse products, manage their cart, and place orders. It also provides an admin interface to manage orders. While the app is fully functional in terms of adding products to the cart and placing orders, future enhancements can improve the user experience and add additional features like authentication and payment processing.
