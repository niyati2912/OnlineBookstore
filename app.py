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

# Book data with diverse genres and prices in USD
BOOKS = [
    {
        "id": 1,
        "title": "The Art of Innovation",
        "author": "Matt Ridley",
        "genre": "Business",
        "price": 29.99,
        "image": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73",
        "description": "A comprehensive guide to innovation and creativity in business."
    },
    {
        "id": 2,
        "title": "Digital Minimalism",
        "author": "Cal Newport",
        "genre": "Self-Help",
        "price": 24.99,
        "image": "https://images.unsplash.com/photo-1555252586-d77e8c828e41",
        "description": "Finding balance in the digital age through minimalism."
    },
    {
        "id": 3,
        "title": "The Midnight Library",
        "author": "Matt Haig",
        "genre": "Fiction",
        "price": 19.99,
        "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570",
        "description": "Between life and death there is a library filled with infinite possibilities."
    },
    {
        "id": 4,
        "title": "Atomic Habits",
        "author": "James Clear",
        "genre": "Self-Help",
        "price": 26.99,
        "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c",
        "description": "Tiny changes, remarkable results: an easy way to build good habits."
    },
    {
        "id": 5,
        "title": "The Silent Patient",
        "author": "Alex Michaelides",
        "genre": "Thriller",
        "price": 22.99,
        "image": "https://images.unsplash.com/photo-1587876931567-564ce588bfbd",
        "description": "A psychological thriller that will keep you guessing until the end."
    },
    {
        "id": 6,
        "title": "Dune",
        "author": "Frank Herbert",
        "genre": "Science Fiction",
        "price": 27.99,
        "image": "https://images.unsplash.com/photo-1589409514187-c21d14df0d04",
        "description": "A masterpiece of science fiction that spans worlds and centuries."
    },
    {
        "id": 7,
        "title": "The Psychology of Money",
        "author": "Morgan Housel",
        "genre": "Finance",
        "price": 21.99,
        "image": "https://images.unsplash.com/photo-1554774853-719586f82d77",
        "description": "Timeless lessons on wealth, greed, and happiness."
    },
    {
        "id": 8,
        "title": "Project Hail Mary",
        "author": "Andy Weir",
        "genre": "Science Fiction",
        "price": 28.99,
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa",
        "description": "A lone astronaut must save humanity from an extinction-level threat."
    },
    {
        "id": 9,
        "title": "The Thursday Murder Club",
        "author": "Richard Osman",
        "genre": "Mystery",
        "price": 23.99,
        "image": "https://images.unsplash.com/photo-1546395227-b15d7e5a3517",
        "description": "Four unlikely friends meet weekly to solve cold cases."
    },
    {
        "id": 10,
        "title": "The Invisible Life of Addie LaRue",
        "author": "V.E. Schwab",
        "genre": "Fantasy",
        "price": 25.99,
        "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794",
        "description": "A woman makes a Faustian bargain to live forever but is cursed to be forgotten by everyone."
    }
]

# Updated Merchandise data with BookNama branding
MERCH = [
    {
        "id": 1,
        "title": "BookNama Literary T-Shirt",
        "category": "Apparel",
        "price": 599.99,
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab",
        "description": "100% cotton t-shirt with BookNama logo and open book design"
    },
    {
        "id": 2,
        "title": "BookNama Reader's Mug",
        "category": "Mugs",
        "price": 299.99,
        "image": "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d",
        "description": "Ceramic mug with BookNama logo and inspirational quote"
    },
    {
        "id": 3,
        "title": "BookNama Bookmark Collection",
        "category": "Accessories",
        "price": 199.99,
        "image": "https://images.unsplash.com/photo-1572371770357-8a26d761d4be",
        "description": "Set of 3 metal bookmarks with BookNama designs and book quotes"
    },
    {
        "id": 4,
        "title": "BookNama Canvas Tote",
        "category": "Bags",
        "price": 399.99,
        "image": "https://images.unsplash.com/photo-1544816155-12df9643f363",
        "description": "Premium canvas tote bag with BookNama logo and book illustration"
    }
]

# Dictionary mapping genres to background images
GENRE_BACKGROUNDS = {
    "Fiction": "https://images.unsplash.com/photo-1516541196182-6bdb0516ed27",
    "Mystery": "https://images.unsplash.com/photo-1501290836517-b22a21c522a4",
    "Science Fiction": "https://images.unsplash.com/photo-1451187580459-43490279c0fa",
    "Fantasy": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23",
    "Business": "https://images.unsplash.com/photo-1507679799987-c73779587ccf",
    "Self-Help": "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e",
    "Thriller": "https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0",
    "Finance": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3"
}

# Get all unique genres
GENRES = sorted(list(set(book["genre"] for book in BOOKS)))

@app.route('/')
def index():
    featured_books = BOOKS[:6]  # Show first 6 books as featured
    featured_merch = MERCH[:2]  # Show first 2 merchandise items
    return render_template('index.html', featured_books=featured_books, featured_merch=featured_merch)

@app.route('/catalog')
def catalog():
    genre = request.args.get('genre', '')
    search = request.args.get('search', '').lower()

    filtered_books = BOOKS
    if genre:
        filtered_books = [book for book in BOOKS if book['genre'].lower() == genre.lower()]
    if search:
        filtered_books = [book for book in filtered_books if search in book['title'].lower() or search in book['author'].lower()]

    background_image = GENRE_BACKGROUNDS.get(genre, "https://images.unsplash.com/photo-1485113771930-4e8b61c60d64")

    return render_template('catalog.html', 
                         books=filtered_books, 
                         genres=GENRES, 
                         selected_genre=genre,
                         background_image=background_image)

@app.route('/merchandise')
def merchandise():
    return render_template('merchandise.html', merch=MERCH)

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