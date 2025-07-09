from flask import Flask, render_template, url_for, request, redirect, session, flash, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

client=MongoClient("mongodb://localhost:27017/")

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

@app.route("/page2")
def page2():
    return render_template("page2.html")

@app.route("/page3")
def page3():
    return render_template("page3.html")

@app.route("/logo")
def logo():
    return render_template("logo.html")
    
# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = accounts.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('add_product'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if accounts.find_one({'username': username}):
            flash('Username already exists', 'error')
            return redirect(url_for('signup'))
            
        hashed_password = generate_password_hash(password)
        user = {
            'username': username,
            'password': hashed_password
        }
        accounts.insert_one(user)
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route("/shop")
def shop():
    items_list = list(items.find({}))
    for item in items_list:
        item['_id'] = str(item['_id'])
    return render_template("shop.html", items=items_list)

@app.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        product = {
            'name': request.form.get('name'),
            'price': float(request.form.get('price')),
            'description': request.form.get('description'),
            'image': request.form.get('image', ''),
            'added_by': session['user_id']
        }
        items.insert_one(product)
        flash('Product added successfully!', 'success')
        return redirect(url_for('shop'))
    return render_template('add_product.html')

@app.route('/delete-product/<product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    try:
        # Check if the product exists and the user has permission to delete it
        product = items.find_one({'_id': ObjectId(product_id)})
        
        if not product:
            return jsonify({'success': False, 'message': 'Product not found'}), 404
            
        # Check if the user is the owner or an admin
        if str(product.get('added_by')) != session['user_id'] and not session.get('is_admin', False):
            return jsonify({'success': False, 'message': 'You do not have permission to delete this product'}), 403
            
        # Delete the product
        result = items.delete_one({'_id': ObjectId(product_id)})
        
        if result.deleted_count == 1:
            return jsonify({'success': True, 'message': 'Product deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete product'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Connect to the database with the correct case
# Note: MongoDB is case-sensitive for database names
db = client['Shop']  # Using bracket notation to match the existing database name

items=db.items
accounts=db.accounts

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

