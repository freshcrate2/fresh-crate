from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.sqlite import JSON

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'), nullable=False)
    cart_details = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship to the Delivery table
    delivery = db.relationship('Delivery', backref=db.backref('orders', lazy=True))


# Initialize the database
@app.before_first_request
def setup():
    db.create_all()
    # Clear existing products (optional)
    Product.query.delete()
    db.session.commit()

    # Add all products
    products = [
        Product(name="Tomatoes", price=20.0),
        Product(name="Potatoes", price=10.0),
        Product(name="Onions", price=15.0),
        Product(name="Carrots", price=25.0),
        Product(name="Ladies Finger", price=30.0),
        Product(name="Cabbage", price=18.0),
        Product(name="Cauliflower", price=22.0),
        Product(name="Spinach", price=12.0),
        Product(name="Broccoli", price=40.0),
        Product(name="Mushrooms", price=50.0),
        Product(name="Capsicum", price=35.0),
        Product(name="Green Chilies", price=15.0),
        Product(name="Peas", price=28.0),
        Product(name="Cucumber", price=12.0),
        Product(name="Garlic", price=60.0),
        Product(name="Ginger", price=50.0),
        Product(name="Beetroot", price=20.0),
        Product(name="Radish", price=18.0),
        Product(name="Pumpkin", price=25.0),
        Product(name="Bottle Gourd", price=15.0),
        Product(name="Bitter Gourd", price=30.0)
    ]

    fruits = [
        Product(name="Mango", price=25.0),
        Product(name="Banana", price=30.0),
        Product(name="Apple", price=50.0),
    ]

    meals = [
        Product(name="Meal_box1", price=100.0),
        Product(name="Mealbox", price=150.0)
    ]

    bevarages = [
        Product(name="Thumsup", price=20.0),
        Product(name="Sprite", price=20.0)
    ]

    dairy = [
        Product(name="Curd 1kg", price=80.0),
        Product(name="Curd 1/2kg", price=40.0)
    ]
    db.session.add_all(products + fruits + meals + bevarages + dairy)
    db.session.commit()

# Routes
@app.route('/')
def signin():
    return render_template('signin.html')

users = []
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        # Basic check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('register'))
        
        # You can add more registration logic here, e.g., store user in database
        users.append({'name': name, 'email': email, 'password': password})

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('home'))  # Redirect to the home page after registration

    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    # Query all products (you can add more filtering conditions if needed)
    products_names = [ "Tomatoes", "Potatoes", "Onions", "Carrots", "Ladies Finger", "Cabbage",  "Cauliflower", "Spinach", "Broccoli", "Mushrooms", "Capsicum", "Green Chilies",  "Peas", "Cucumber", "Garlic", "Ginger", "Beetroot", "Radish", "Pumpkin", "Bottle Gourd", "Bitter Gourd"]
    products = Product.query.filter(Product.name.in_(products_names)).all()
    
    return render_template('index.html', products=products)

@app.route('/fruit')
def fruit():
    # List of known fruit names
    fruit_names = ["Mango", "Banana", "Apple"]  # Add more fruit names as needed
    
    # Query products that match any of the fruit names
    fruits = Product.query.filter(Product.name.in_(fruit_names)).all()
    
    return render_template('index.html', products=fruits)

@app.route('/dairys')
def dairys():
    # List of known fruit names
    dairy_names = ["Curd 1kg", "Curd 1/2kg"]  # Add more fruit names as needed
    
    # Query products that match any of the fruit names
    dairy = Product.query.filter(Product.name.in_(dairy_names)).all()
    
    return render_template('index.html', products=dairy)

@app.route('/meal')
def meal():
    # List of known meal names
    meal_names = ["Meal_box1", "Mealbox"]  # Add more meal names as needed
    
    # Query products that match any of the meal names
    meals = Product.query.filter(Product.name.in_(meal_names)).all()
    
    return render_template('index.html', products=meals)

@app.route('/bevarage')
def bevarage():
    # List of known meal names
    bevarage_names = ["Thumsup", "Sprite"]  # Add more meal names as needed
    
    # Query products that match any of the meal names
    bevarages = Product.query.filter(Product.name.in_(bevarage_names)).all()
    
    return render_template('index.html', products=bevarages)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    
    if 'cart' not in session:
        session['cart'] = []
    
    # Get the cart items from the session
    cart = session['cart']
    
    # Check if the product is already in the cart
    product_found = False
    for item in cart:
        if item['id'] == product.id:
            item['quantity'] += 1  # Increment the quantity if product is already in cart
            product_found = True
            break
    
    # If product is not found, add it to the cart with quantity 1
    if not product_found:
        cart.append({'id': product.id, 'name': product.name, 'price': product.price, 'quantity': 1})
    
    session['cart'] = cart  # Update the session with the new cart
    flash(f"{product.name} added to cart!", "success")  # Flash message for the user
    return redirect(url_for('cart'))  # Redirect to the cart page

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    session['cart'] = [item for item in cart if item['id'] != product_id]
    flash("Item removed from cart!", "success")
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    
    # Ensure quantity exists for all cart items and calculate total cost
    for item in cart_items:
        if 'quantity' not in item:
            item['quantity'] = 1  # If quantity is missing, set it to 1
    
    # Calculate the total cost by considering the quantity
    total_cost = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template('cart.html', cart=cart_items, total_cost=total_cost)

@app.route('/delivery', methods=['GET', 'POST'])
def delivery():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']

        # Get cart items from the session
        cart_items = session.get('cart', [])

        # Ensure quantity exists for all cart items and calculate total cost
        for item in cart_items:
            if 'quantity' not in item:
                item['quantity'] = 1  # If quantity is missing, set it to 1

        # Calculate the total cost of the cart, accounting for quantity
        total_cost = sum(item['price'] * item['quantity'] for item in cart_items)

        # Define shipping charges (you can change this logic)
        shipping_charge = 10.0  # Static shipping charge, or calculate based on cart value or location

        # Calculate the total order amount (items + shipping)
        total_order_amount = total_cost + shipping_charge

        # Save delivery details to the database
        new_delivery = Delivery(name=name, address=address, phone=phone)
        db.session.add(new_delivery)
        db.session.commit()

        # Create an order entry for the newly created delivery
        new_order = Order(
            delivery_id=new_delivery.id,
            cart_details=cart_items
        )
        db.session.add(new_order)
        db.session.commit()

        flash(f"Order placed successfully! Total amount: ₹{total_order_amount}", "success")
        session.pop('cart', None)  # Clear the cart
        return redirect(url_for('home'))

    # If the request is GET, calculate the total cost and shipping charges for displaying on the delivery page
    cart_items = session.get('cart', [])
    
    # Ensure quantity exists for all cart items and calculate total cost
    for item in cart_items:
        if 'quantity' not in item:
            item['quantity'] = 1  # If quantity is missing, set it to 1

    # Calculate the total cost of the cart, accounting for quantity
    total_cost = sum(item['price'] * item['quantity'] for item in cart_items)

    # Define shipping charges (you can change this logic)
    shipping_charge = 10.0  # Static shipping charge

    # Calculate the total order amount (items + shipping)
    total_order_amount = total_cost + shipping_charge

    return render_template('delivery.html', cart_items=cart_items, total_cost=total_cost, shipping_charge=shipping_charge, total_order_amount=total_order_amount)


@app.route('/place_order', methods=['POST'])
def place_order():
    if 'cart' not in session or not session['cart']:
        flash("Your cart is empty!", "error")
        return redirect(url_for('cart'))

    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    
    # Convert cart items to a string for storage
    cart_items = session['cart']
    cart_items_str = ', '.join([f"{item['name']} (x{item.get('quantity', 1)})" for item in cart_items])

    # Save the order to the database
    new_delivery = Delivery(name=name, address=address, phone=phone)
    db.session.add(new_delivery)
    db.session.commit()

    new_order = Order(
        delivery_id=new_delivery.id,
        cart_details=cart_items
    )
    db.session.add(new_order)
    db.session.commit()

    # Clear the cart after order placement
    session.pop('cart', None)

    flash("Order placed successfully!", "success")
    return redirect(url_for('index'))

@app.route('/owner_orders')
def owner_orders():
    # Fetch all orders from the database, ordered by most recent
    orders = Order.query.order_by(Order.created_at.desc()).all()  # Fetching orders in reverse order (most recent first)
    return render_template('owner_orders.html', orders=orders)

@app.route('/order/<int:order_id>')
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    delivery = Delivery.query.get_or_404(order.delivery_id)
    return render_template('order_details.html', order=order, delivery=delivery)

if __name__ == '__main__':
    app.run(debug=True)
