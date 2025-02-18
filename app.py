import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import json

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///bookstore.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

# Mock book data with prices in rupees
BOOKS = [
    {
        "id": 1,
        "title": "The Art of Innovation",
        "author": "Matt Ridley",
        "price": 2499.00,  # Price in INR
        "image": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73",
        "description": "A comprehensive guide to innovation and creativity in business."
    },
    {
        "id": 2,
        "title": "Digital Minimalism",
        "author": "Thought Catalog",
        "price": 1999.00,  # Price in INR
        "image": "https://images.unsplash.com/photo-1555252586-d77e8c828e41",
        "description": "Finding balance in the digital age."
    }
]

@app.route('/')
def index():
    featured_books = BOOKS[:4]  # First 4 books as featured
    return render_template('index.html', featured_books=featured_books)

@app.route('/catalog')
def catalog():
    search = request.args.get('search', '').lower()
    if search:
        filtered_books = [book for book in BOOKS if search in book['title'].lower() or search in book['author'].lower()]
    else:
        filtered_books = BOOKS
    return render_template('catalog.html', books=filtered_books)

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = next((book for book in BOOKS if book['id'] == book_id), None)
    if book is None:
        flash('Book not found!', 'error')
        return redirect(url_for('catalog'))
    return render_template('book_detail.html', book=book)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    cart_books = []
    total = 0
    for item in cart_items:
        book = next((book for book in BOOKS if book['id'] == item['id']), None)
        if book:
            quantity = item['quantity']
            book_total = book['price'] * quantity
            total += book_total
            cart_books.append({**book, 'quantity': quantity, 'total': book_total})
    return render_template('cart.html', cart_items=cart_books, total=total)

@app.route('/add_to_cart/<int:book_id>', methods=['POST'])
def add_to_cart(book_id):
    if 'cart' not in session:
        session['cart'] = []
    
    cart = session['cart']
    item = next((item for item in cart if item['id'] == book_id), None)
    
    if item:
        item['quantity'] += 1
    else:
        cart.append({'id': book_id, 'quantity': 1})
    
    session['cart'] = cart
    flash('Book added to cart!', 'success')
    return redirect(request.referrer or url_for('catalog'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Mock checkout process
        session['cart'] = []
        flash('Order placed successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('checkout.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)