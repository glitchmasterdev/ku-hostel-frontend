import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Drop existing table if migrating from older schema
    c.execute('DROP TABLE IF EXISTS students')

    # Create students table
    c.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            gender TEXT NOT NULL,
            year_of_study TEXT NOT NULL,
            phone TEXT,
            school TEXT,
            disability_status TEXT DEFAULT 'None',
            application_status TEXT DEFAULT 'Pending',
            allocated_hostel TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample data matching the original test cases
    sample_students = [
        ('J17/1234/2026', 'Amina Wanjiru', 'Female', '1', '0712345678', 'School of Engineering', 'None', 'Allocated', 'Nyayo Hostel Block A - Room 204'),
        ('J17/5678/2026', 'Brian Ochieng', 'Male', '2', '0723456789', 'School of Business', 'None', 'Allocated', 'Hall 11 - Room 312'),
        ('J17/9101/2026', 'Catherine Muthoni', 'Female', '3', '0734567890', 'School of Pure & Applied Sciences', 'None', 'Allocated', 'Nyayo Hostel Block C - Room 115'),
        ('J17/1122/2026', 'David Kipchoge', 'Male', '1', '0745678901', 'School of Education', 'Physical', 'Allocated', 'Hall 9 - Room 101 (Accessible)'),
        ('J17/3344/2026', 'Esther Njeri', 'Female', '4', '0756789012', 'School of Law', 'None', 'Pending', None),
        ('J17/5566/2026', 'Francis Kamau', 'Male', '2', '0767890123', 'School of Medicine', 'None', 'Pending', None)
    ]

    c.executemany('''
        INSERT INTO students (student_id, full_name, gender, year_of_study, phone, school, disability_status, application_status, allocated_hostel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_students)

    conn.commit()
    conn.close()
    print("Database initialized successfully with test data.")

if __name__ == '__main__':
    init_db()
