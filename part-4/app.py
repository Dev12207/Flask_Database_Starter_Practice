"""
Part 4: REST API with Flask
===========================
Build a JSON API for database operations (used by frontend apps, mobile apps, etc.)

What You'll Learn:
- REST API concepts (GET, POST, PUT, DELETE)
- JSON responses with jsonify
- API error handling
- Status codes
- Testing APIs with curl or Postman

Prerequisites: Complete part-3 (SQLAlchemy)
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# =============================================================================
# MODELS
# =============================================================================

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)
    isbn = db.Column(db.String(20), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):  # Convert model to dictionary for JSON response
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'isbn': self.isbn,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# =============================================================================
# REST API ROUTES
# =============================================================================

# GET /api/books - Get all books with sorting and pagination
@app.route('/api/books', methods=['GET'])
def get_books():
    # 1. Get query parameters for sorting
    sort_column = request.args.get('sort', 'id')  # Default sort by ID
    order = request.args.get('order', 'asc')      # Default order is ascending

    # 2. Get query parameters for pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # 3. Build the base query
    query = Book.query

    # 4. Apply Sorting logic
    # Check if the requested column exists in the Book model to avoid errors
    if hasattr(Book, sort_column):
        col = getattr(Book, sort_column)
        if order.lower() == 'desc':
            query = query.order_by(col.desc())
        else:
            query = query.order_by(col.asc())

    # 5. Apply Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    books = pagination.items

    return jsonify({
        'success': True,
        'count': len(books),
        'total_books': pagination.total,
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'sort': sort_column,
        'order': order,
        'books': [book.to_dict() for book in books]
    })


# GET /api/books/<id> - Get single book
@app.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({
            'success': False,
            'error': 'Book not found'
        }), 404  # Return 404 status code

    return jsonify({
        'success': True,
        'book': book.to_dict()
    })


# POST /api/books - Create new book
@app.route('/api/books', methods=['POST'])
def create_book():
    data = request.get_json()  # Get JSON data from request body

    # Validation
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    if not data.get('title') or not data.get('author'):
        return jsonify({'success': False, 'error': 'Title and author are required'}), 400

    # Check for duplicate ISBN
    if data.get('isbn'):
        existing = Book.query.filter_by(isbn=data['isbn']).first()
        if existing:
            return jsonify({'success': False, 'error': 'ISBN already exists'}), 400

    # Create book
    new_book = Book(
        title=data['title'],
        author=data['author'],
        year=data.get('year'),  # Optional field
        isbn=data.get('isbn')
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Book created successfully',
        'book': new_book.to_dict()
    }), 201  # 201 = Created


# PUT /api/books/<id> - Update book
@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({'success': False, 'error': 'Book not found'}), 404

    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    # Update fields if provided
    if 'title' in data:
        book.title = data['title']
    if 'author' in data:
        book.author = data['author']
    if 'year' in data:
        book.year = data['year']
    if 'isbn' in data:
        book.isbn = data['isbn']

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Book updated successfully',
        'book': book.to_dict()
    })


# DELETE /api/books/<id> - Delete book
@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)

    if not book:
        return jsonify({'success': False, 'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Book deleted successfully'
    })


# =============================================================================
# BONUS: Search and Filter
# =============================================================================

# GET /api/books/search?q=python&author=john
@app.route('/api/books/search', methods=['GET'])
def search_books():
    query = Book.query

    # Filter by title (partial match)
    title = request.args.get('q')  # Query parameter: ?q=python
    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))  # Case-insensitive LIKE

    # Filter by author
    author = request.args.get('author')
    if author:
        query = query.filter(Book.author.ilike(f'%{author}%'))

    # Filter by year
    year = request.args.get('year')
    if year:
        query = query.filter_by(year=int(year))

    books = query.all()

    return jsonify({
        'success': True,
        'count': len(books),
        'books': [book.to_dict() for book in books]
    })


# =============================================================================
# SIMPLE WEB PAGE FOR TESTING
# =============================================================================

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Part 4 - Book Manager</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; margin: 40px; background: #1a1a2e; color: #eee; }
            .container { max-width: 1000px; margin: auto; }
            h1 { color: #e94560; border-bottom: 2px solid #e94560; padding-bottom: 10px; }
            .card { background: #16213e; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
            input { padding: 8px; margin: 5px; border-radius: 4px; border: none; background: #0f3460; color: white; width: 150px; }
            button { padding: 8px 15px; border-radius: 4px; border: none; cursor: pointer; font-weight: bold; margin: 2px; }
            .btn-add { background: #27ae60; color: white; }
            .btn-edit { background: #3498db; color: white; }
            .btn-save { background: #f1c40f; color: #1a1a2e; }
            .btn-delete { background: #e74c3c; color: white; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th { text-align: left; background: #0f3460; padding: 12px; }
            td { padding: 12px; border-bottom: 1px solid #0f3460; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Book Inventory Manager</h1>
            
            <div class="card">
                <h3>Add New Book</h3>
                <input type="text" id="title" placeholder="Title">
                <input type="text" id="author" placeholder="Author">
                <input type="text" id="isbn" placeholder="ISBN">
                <button class="btn-add" onclick="addBook()">Add Book</button>
            </div>

            <div class="card">
                <h3>Current Inventory</h3>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Title</th>
                            <th>Author</th>
                            <th>ISBN</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="book-table"></tbody>
                </table>
            </div>
        </div>

        <script>
            // 1. FETCH AND DISPLAY
            async function fetchBooks() {
                const response = await fetch('/api/books');
                const data = await response.json();
                const tableBody = document.getElementById('book-table');
                tableBody.innerHTML = '';

                data.books.forEach(book => {
                    tableBody.innerHTML += `
                        <tr id="row-${book.id}">
                            <td>${book.id}</td>
                            <td class="title-cell">${book.title}</td>
                            <td class="author-cell">${book.author}</td>
                            <td class="isbn-cell">${book.isbn || ''}</td>
                            <td>
                                <button class="btn-edit" onclick="enableEdit(${book.id})">Edit</button>
                                <button class="btn-delete" onclick="deleteBook(${book.id})">Delete</button>
                            </td>
                        </tr>
                    `;
                });
            }

            // 2. ENABLE INLINE EDITING
            function enableEdit(id) {
                const row = document.getElementById(`row-${id}`);
                const title = row.querySelector('.title-cell').innerText;
                const author = row.querySelector('.author-cell').innerText;
                const isbn = row.querySelector('.isbn-cell').innerText;

                row.innerHTML = `
                    <td>${id}</td>
                    <td><input type="text" id="edit-title-${id}" value="${title}"></td>
                    <td><input type="text" id="edit-author-${id}" value="${author}"></td>
                    <td><input type="text" id="edit-isbn-${id}" value="${isbn}"></td>
                    <td>
                        <button class="btn-save" onclick="updateBook(${id})">Save</button>
                        <button onclick="fetchBooks()">Cancel</button>
                    </td>
                `;
            }

            // 3. UPDATE BOOK (PUT REQUEST)
            async function updateBook(id) {
                const updatedData = {
                    title: document.getElementById(`edit-title-${id}`).value,
                    author: document.getElementById(`edit-author-${id}`).value,
                    isbn: document.getElementById(`edit-isbn-${id}`).value
                };

                const response = await fetch('/api/books/' + id, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updatedData)
                });

                if (response.ok) {
                    fetchBooks();
                } else {
                    alert("Failed to update book.");
                }
            }

            async function addBook() {
                const title = document.getElementById('title').value;
                const author = document.getElementById('author').value;
                const isbn = document.getElementById('isbn').value;
                await fetch('/api/books', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title, author, isbn })
                });
                fetchBooks();
            }

            async function deleteBook(id) {
                if (confirm('Delete?')) {
                    await fetch('/api/books/' + id, { method: 'DELETE' });
                    fetchBooks();
                }
            }

            fetchBooks();
        </script>
    </body>
    </html>
    '''
# =============================================================================
# INITIALIZE DATABASE WITH SAMPLE DATA
# =============================================================================

def init_db():
    with app.app_context():
        db.create_all()

        if Book.query.count() == 0:
            sample_books = [
                Book(title='Python Crash Course', author='Eric Matthes', year=2019, isbn='978-1593279288'),
                Book(title='Flask Web Development', author='Miguel Grinberg', year=2018, isbn='978-1491991732'),
                Book(title='Clean Code', author='Robert C. Martin', year=2008, isbn='978-0132350884'),
            ]
            db.session.add_all(sample_books)
            db.session.commit()
            print('Sample books added!')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)


# =============================================================================
# REST API CONCEPTS:
# =============================================================================
#
# HTTP Method | CRUD      | Typical Use
# ------------|-----------|---------------------------
# GET         | Read      | Retrieve data
# POST        | Create    | Create new resource
# PUT         | Update    | Update entire resource
# PATCH       | Update    | Update partial resource
# DELETE      | Delete    | Remove resource
#
# =============================================================================
# HTTP STATUS CODES:
# =============================================================================
#
# Code | Meaning
# -----|------------------
# 200  | OK (Success)
# 201  | Created
# 400  | Bad Request (client error)
# 404  | Not Found
# 500  | Internal Server Error
#
# =============================================================================
# KEY FUNCTIONS:
# =============================================================================
#
# jsonify()           - Convert Python dict to JSON response
# request.get_json()  - Get JSON data from request body
# request.args.get()  - Get query parameters (?key=value)
#
# =============================================================================


# =============================================================================
# EXERCISE:
# =============================================================================
#
# 1. Add pagination: `/api/books?page=1&per_page=10`
# 2. Add sorting: `/api/books?sort=title&order=desc`
# 3. Create a simple frontend using JavaScript fetch()
#
# =============================================================================
