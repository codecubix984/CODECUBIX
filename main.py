import sqlite3

conn = sqlite3.connect('codecubix.db')

cur = conn.cursor()

print('file was created')
cur.execute('''CREATE TABLE bmi
(name TEXT,
weight REAL,
height INT,
bmi TEXT,
body_type TEXT);''')
# cur.execute('CREATE TABLE codecubix_record(id INTEGER, name TEXT, number INTEGER);')
print('bmi table created')
conn.commit()
conn.close()