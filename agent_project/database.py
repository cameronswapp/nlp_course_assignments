import sqlite3
from faker import Faker


fake = Faker()


conn = sqlite3.connect('aggies.db')
cur = conn.cursor()

# Create tables
cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grad_year INTEGER NOT NULL
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS grades (
        grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT,
        grade TEXT,
        FOREIGN KEY(student_id) REFERENCES students(student_id)
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS sports (
        sport_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sport_name TEXT NOT NULL
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS student_sports (
        student_id INTEGER,
        sport_id INTEGER,
        jersey_number INTEGER,
        championships_won INTEGER,
        position TEXT,
        years_played INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(student_id),
        FOREIGN KEY(sport_id) REFERENCES sports(sport_id)
    );
""")
# Insert into table
studentData = [
    ('Jordan Love', 2019),
    ('Bobby Wagner', 2012),
    ('Merlin Olsen', 1962),
    ('Bryson Barnes', 2026),
    ('Jaycee Carroll', 2008),
    ('Darius Brown', 2024),
    ('Logan Bonner', 2022),
    ('Taylor Funk', 2023),
    ('Mason Falslev', 2027),
    ('Karson Templin', 2027),
    ('Tierney Barlow', 2026),
    ('Cheyenne Stubbs', 2025),
    ('Tatum Stall', 2025),
    ('Taylor Rath', 2026),
    ('Ian Martinez', 2025),
    ('Drake Allen', 2026)
]

studentData.extend([
    (fake.name(), fake.random_int(min=2000, max=2025))
    for _ in range(100)
])

cur.executemany("INSERT INTO students (name, grad_year) VALUES (?, ?)", studentData)

gradesData = []
subjects = ['Math', 'Science', 'History', 'English', 'Art', 'Physical Education']
grades = ['A', 'B', 'C', 'D', 'F']
gradesData.extend([
    (fake.random_int(min = 1, max = len(studentData)), fake.random_element(subjects), fake.random_element(grades))
    for _ in range(300)
])

cur.executemany("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)", gradesData)

sportsData = [
    ('Football',),
    ('Basketball(M)',),
    ('Basketball(W)',),
    ('Soccer',),
    ('Volleyball',)
]

cur.executemany("INSERT INTO sports (sport_name) VALUES (?)", sportsData)

studentSportsData = [
    (1, 1, 10, 0, 'Quarterback', 3),
    (2, 1, 9, 1, 'Linebacker', 4),
    (3, 1, 71, 1, 'Tackle', 4),
    (4, 1, 16, 0, 'Quarterback', 2),
    (5, 2, 20, 2, 'Guard', 4),
    (6, 2, 10, 1, 'Guard', 1),
    (7, 1, 1, 1, 'Quarterback', 2),
    (8, 2, 23, 0, 'Forward', 1),
    (9, 2, 12, 1, 'Guard', 3),
    (10, 2, 24, 1, 'Center', 3),
    (11, 5, 2, 1, 'Outside Hitter', 2),
    (12, 3, 24, 0, 'Guard', 2),
    (13, 5, 2, 2, 'Outside Hitter', 4),
    (14, 4, 0, 1, 'Goalkeeper', 1),
    (15, 2, 4, 1, 'Forward', 2),
    (16, 2, 8, 0, 'Guard', 2)
]
positions = ['Forward', 'Guard', 'Center', 'Quarterback', 'Linebacker', 'Goalkeeper', 'Outside Hitter']
for i in range(17, len(studentData) + 1):
    studentSportsData.extend([
        (
            i,
            fake.random_int(min = 1, max = len(sportsData)),
            fake.random_int(min = 0, max = 99),
            fake.random_int(min = 0, max = 4),
            fake.random_element(positions),
            fake.random_int(min = 1, max = 4)
        )
    ])

cur.executemany("INSERT INTO student_sports (student_id, sport_id, jersey_number, championships_won, position, years_played) VALUES (?, ?, ?, ?, ?, ?)", studentSportsData)

conn.commit()
conn.close()
