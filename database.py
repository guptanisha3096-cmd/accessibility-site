import sqlite3

def get_db():
    conn = sqlite3.connect(':memory:')
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

    # Seed data - permanent places (name, category, area, description)
    places_data = [
        ("Government Hospital(Kacheri Rd)", "Hospital", "Palghar", "Government hospital with ramp, accessible toilet, parking, and seating. Elevator not yet verified."),
        ("District Collector Office", "Government Office", "Palghar", "Government office with ramp, parking, seating, elevator and accessible toilet."),
        ("Palghar Railway Station", "Railway Station", "Palghar", "Major railway station with full accessibility - ramps, elevators, accessible toilets, parking, and seating available."),
        ("St.John College", "College", "Palghar", "College with elevators, parking, and seating and toilet. wheelchair ramp not available."),
        ("Palghar Bus Depot", "Bus station", "Palghar", "Government bus depot with accessible toilets, parking, and seating. Ramp available, no elevator."),
        ("Palghar Court", "Government Office", "Palghar", "District court with ramp, accessible toilet, parking, and seating. Elevator not yet verified."),
        ("Palghar Post Office", "Government Office", "Palghar", "Government office with ramp, accessible toilet, parking, and seating. Elevator not yet verified."),
        ("Palghar Police Station", "Government Office", "Palghar", "Police station with ramp, accessible toilet, parking, and seating. Elevator not yet verified."),
        ("The Royal Family Restaurant", "Restaurant", "Palghar", "The Royal Family Restaurant: Family-friendly restaurant offering a variety of Indian and local dishes in a comfortable dining environment. Ramp, toilet, parking, and seating available; elevator not available."),
        ("Rasam Restaurant", "Restaurant", "Palghar", "The Family Restaurant: Family-friendly restaurant offering a variety of Indian and local dishes in a comfortable dining environment. Ramp, parking, and seating available; elevator and toilet not available."),
        ("Viva Celebration Restaurant", "Restaurant", "Palghar", "Family Restaurant offering a variety of food option. Ramp, toilet, parking, and seating available; elevator not available."),
        ("Dandekar College", "College", "Palghar", "College in Palghar with parking and seating available. Elevator and wheelchair ramp are not available.")
    ]
    count = conn.execute('SELECT COUNT(*) FROM places').fetchone()[0]
    if count == 0:
        for place in places_data:
            conn.execute("INSERT INTO places (name, category, area, description) VALUES (?, ?, ?, ?)", place)

    conn.commit()
    conn.close()