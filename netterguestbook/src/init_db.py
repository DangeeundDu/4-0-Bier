import sqlite3
con = sqlite3.connect('database.db')

cur = con.cursor()

cur.execute('''CREATE TABLE post
               (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, is_public INTEGER, secret TEXT, message TEXT, image_path TEXT)''')

cur.execute("INSERT INTO post (date, is_public, message) VALUES ('May 26 2021 12:21:50', 1, 'Welcome to the netterguestbook!')")
con.commit()
con.close()

