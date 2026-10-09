from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def get_db():
    conn = sqlite3.connect('accessibility.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    places = conn.execute('SELECT * FROM places').fetchall()
    conn.close()
    return render_template('index.html', places=places)

@app.route('/search')
def search():
    q = request.args.get('q', '')
    facility = request.args.get('facility', '')
    conn = get_db()
    if facility and facility != 'All':
        places = conn.execute('''SELECT DISTINCT p.* FROM places p
            JOIN facilities f ON f.place_id = p.id
            WHERE f.facility_type = ? AND f.available = 'Yes'
            AND (p.name LIKE ? OR p.category LIKE ? OR p.area LIKE ?)''',
            (facility, f'%{q}%', f'%{q}%', f'%{q}%')).fetchall()
    else:
        places = conn.execute('''SELECT * FROM places
            WHERE name LIKE ? OR category LIKE ? OR area LIKE ?''',
            (f'%{q}%', f'%{q}%', f'%{q}%')).fetchall()
    conn.close()
    return render_template('index.html', places=places)

@app.route('/place/<int:place_id>')
def place_detail(place_id):
    conn = get_db()
    place = conn.execute('SELECT * FROM places WHERE id = ?', (place_id,)).fetchone()
    facilities = conn.execute('SELECT * FROM facilities WHERE place_id = ?', (place_id,)).fetchall()
    reviews = conn.execute('SELECT * FROM reviews WHERE place_id = ?', (place_id,)).fetchall()
    conn.close()
    return render_template('place.html', place=place, facilities=facilities, reviews=reviews)

@app.route('/place/<int:place_id>/review', methods=['POST'])
def add_review(place_id):
    user_name = request.form.get('user_name', 'Anonymous')
    rating = request.form.get('rating', 5)
    comment = request.form.get('comment', '')
    conn = get_db()
    conn.execute('INSERT INTO reviews (place_id, user_name, rating, comment) VALUES (?, ?, ?, ?)',
                 (place_id, user_name, rating, comment))
    conn.commit()
    conn.close()
    return redirect(url_for('place_detail', place_id=place_id))

@app.route('/place/<int:place_id>/report', methods=['POST'])
def report_problem(place_id):
    problem = request.form.get('problem', '')
    conn = get_db()
    conn.execute('INSERT INTO reports (place_id, problem) VALUES (?, ?)', (place_id, problem))
    conn.commit()
    conn.close()
    return redirect(url_for('place_detail', place_id=place_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

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
if __name__ == '__main__':
    from database import init_db
    init_db()
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))