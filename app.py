from flask import Flask, render_template, url_for, jsonify,request
import sqlite3


app = Flask(__name__)

app = Flask(__name__, static_folder='static')

# Define the route for the add_book page
@app.route('/add_book')
def add_book1():
    return render_template('add_book.html')

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/search_book')
def search_book1():
    return render_template('search_book.html')



def create_table():
    # Connect to the database
    conn = sqlite3.connect('books.db')
    # Create a cursor-
    cursor = conn.cursor()
    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
    table_exists = cursor.fetchone()
    # Create the table if it doesn't exist
    if not table_exists:
        cursor.execute('''
            CREATE TABLE books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                genre TEXT
            )
        ''')
        conn.commit()
    # Close the connection
    conn.close()

create_table()





@app.route('/add_book', methods=['POST'])
def add_book():
    # Get the book data from the request
    data = request.json
    title = data['title']
    author = data['author']
    genre = data['genre']

    # Insert the new book into the database
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author, genre) VALUES (?, ?, ?)", (title, author, genre))
    conn.commit()
    conn.close()

    # Return a response indicating success
    return jsonify({'status': 'success'})


@app.route('/books', methods=['GET'])
def get_books():
    # Get the search query from the URL parameters
    search_query = request.args.get("search")

    # Get the list of books from the database
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    if search_query:
        # Search for books by title
        c.execute("SELECT * FROM books WHERE title LIKE ?", ('%'+search_query+'%',))
    else:
        # Get all books
        c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()

    # Convert the list of books to a JSON object and return it
    return jsonify({'books': books})








@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    # Delete the book from the database
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (book_id,)) 
    conn.commit()
    conn.close()

    # Return a response indicating success or failure
    response = {'status': 'success'}
    status_code = 200
    return jsonify(response), status_code




@app.route('/search')
def search_book():
    #
    search_query = request.args.get('query')
    # Query the database for books that match the search query
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", ('%' + search_query + '%', '%' + search_query + '%'))
    books = c.fetchall()
    conn.close()
    
    # Render the search results page
    return render_template('search_book.html', books=books, query=search_query)






app.run(debug=True)



