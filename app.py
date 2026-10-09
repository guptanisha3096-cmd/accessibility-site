from flask import Flask, render_template, request, redirect, url_for, session
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Call init_db() at startup so the database is always created
init_db()

@app.route('/')
def index():
    conn = get_db()
    places = conn.execute('SELECT * FROM places').fetchall()
    conn.close()
    return render_template('index.html', places=places)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    facility = request.args.get('facility', '')
    conn = get_db()
    if query:
        places = conn.execute("SELECT * FROM places WHERE name LIKE ?", ('%' + query + '%',)).fetchall()
    else:
        places = conn.execute('SELECT * FROM places').fetchall()
    conn.close()
    return render_template('index.html', places=places)

@app.route('/place/<int:place_id>')
def place(place_id):
    conn = get_db()
    place = conn.execute('SELECT * FROM places WHERE id = ?', (place_id,)).fetchone()
    facilities = conn.execute('SELECT * FROM facilities WHERE place_id = ?', (place_id,)).fetchall()
    reviews = conn.execute('SELECT * FROM reviews WHERE place_id = ?', (place_id,)).fetchall()
    conn.close()
    return render_template('place.html', place=place, facilities=facilities, reviews=reviews)

@app.route('/add_place', methods=['GET', 'POST'])
def add_place():
    if not session.get('admin'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        area = request.form.get('area')
        description = request.form.get('description')
        conn = get_db()
        cur = conn.execute('INSERT INTO places (name, category, area, description) VALUES (?, ?, ?, ?)',
                           (name, category, area, description))
        place_id = cur.lastrowid
        facilities = ['Ramp', 'Elevator', 'Toilet', 'Parking', 'Seating']
        for f in facilities:
            available = request.form.get(f, 'No')
            conn.execute('INSERT INTO facilities (place_id, facility_type, available) VALUES (?, ?, ?)',
                         (place_id, f, available))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_place.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('add_place'))
    return render_template('login.html')

@app.route('/review/<int:place_id>', methods=['POST'])
def review(place_id):
    user_name = request.form.get('user_name')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    conn = get_db()
    conn.execute('INSERT INTO reviews (place_id, user_name, rating, comment) VALUES (?, ?, ?, ?)',
                 (place_id, user_name, rating, comment))
    conn.commit()
    conn.close()
    return redirect(url_for('place', place_id=place_id))

@app.route('/report/<int:place_id>', methods=['POST'])
def report(place_id):
    problem = request.form.get('problem')
    conn = get_db()
    conn.execute('INSERT INTO reports (place_id, problem) VALUES (?, ?)',
                 (place_id, problem))
    conn.commit()
    conn.close()
    return redirect(url_for('place', place_id=place_id))

if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))