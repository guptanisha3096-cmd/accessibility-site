import sqlite3
import os

DATABASE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'accessibility.db'
)

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    conn.execute('''CREATE TABLE IF NOT EXISTS places (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        area TEXT NOT NULL,
        description TEXT
    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS facilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place_id INTEGER NOT NULL,
        facility_type TEXT NOT NULL,
        available TEXT NOT NULL
    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place_id INTEGER NOT NULL,
        user_name TEXT,
        rating INTEGER,
        comment TEXT
    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        place_id INTEGER NOT NULL,
        problem TEXT,
        status TEXT DEFAULT 'pending'
    )''')

    places_data = [
        ("Government Hospital(Kacheri Rd)", "Hospital", "Palghar",
         "Government hospital with ramp, accessible toilet, parking, and seating. Elevator not yet verified."),
        ("District Collector Office", "Government Office", "Palghar",
         "Government office with ramp, parking, seating, elevator and accessible toilet."),
        ("Palghar Railway Station", "Railway Station", "Palghar",
         "Major railway station with ramps, elevators, accessible toilets, parking, and seating."),
        ("St.John College", "College", "Palghar",
         "College with elevators, parking, seating and toilet. Wheelchair ramp not available."),
        ("Palghar Bus Depot", "Bus station", "Palghar",
         "Government bus depot with accessible toilets, parking, seating and ramp. No elevator."),
        ("Palghar Court", "Government Office", "Palghar",
         "District court with ramp, accessible toilet, parking, and seating."),
        ("Palghar Post Office", "Government Office", "Palghar",
         "Government office with ramp, accessible toilet, parking, and seating."),
        ("Palghar Police Station", "Government Office", "Palghar",
         "Police station with ramp, accessible toilet, parking, and seating."),
        ("The Royal Family Restaurant", "Restaurant", "Palghar",
         "Family restaurant with ramp, toilet, parking, and seating. No elevator."),
        ("Rasam Restaurant", "Restaurant", "Palghar",
         "Family restaurant with ramp, parking, and seating. No elevator or toilet."),
        ("Viva Celebration Restaurant", "Restaurant", "Palghar",
         "Family restaurant with ramp, toilet, parking, and seating. No elevator."),
        ("Dandekar College", "College", "Palghar",
         "College with parking and seating. No elevator or wheelchair ramp.")
    ]

    count = conn.execute(
        'SELECT COUNT(*) FROM places'
    ).fetchone()[0]

    if count == 0:
        conn.executemany(
            '''INSERT INTO places
            (name, category, area, description)
            VALUES (?, ?, ?, ?)''',
            places_data
        )

    conn.commit()
    conn.close()