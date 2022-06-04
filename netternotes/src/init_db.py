import sqlite3

connection = sqlite3.connect('database.db')

cur = connection.cursor()

cur.execute("DROP TABLE IF EXISTS notes;")

cur.execute("CREATE TABLE notes (id INTEGER PRIMARY KEY AUTOINCREMENT, created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, locked INTEGER, title TEXT, subtitle TEXT, message TEXT, note_password TEXT)")

cur.execute("INSERT INTO notes (locked, title, subtitle, message) VALUES (?,?,?,?)", (0, 'TODO', 'urgent', 'To Do: Call back Johanna'))
cur.execute("INSERT INTO notes (locked, title, subtitle, message) VALUES (?,?,?,?)", (0, 'TODO', ' VERY urgent','To Do: research password manager'))
cur.execute("INSERT INTO notes (locked, title, subtitle, message) VALUES (?,?,?,?)", (0, 'Ideas', 'very good food', 'Restaurant Recommendations: NETTERfood, Flying Pasta and Galaxy Coffee'))
cur.execute("INSERT INTO notes (locked, title, subtitle, message) VALUES (?,?,?,?)", (0, 'Confidential', 'should delete asap', 'pa55word'))
cur.execute("INSERT INTO notes (locked, title, subtitle, message) VALUES (?,?,?,?)", (0, 'Confidential', 'should delete asap', 'PIN: 6378'))
cur.execute("INSERT INTO notes (locked, title, subtitle, message) VALUES (?,?,?,?)", (0, 'Confidential', 'should delete asap', 'pCk8MEptFN'))
cur.execute("INSERT INTO notes (locked, title, subtitle, message) VALUES (?,?,?,?)", (0, 'Confidential', 'should delete asap', 'UXF9hdf8xv'))
cur.execute("INSERT INTO notes (locked, title, subtitle, message) VALUES (?,?,?,?)", (0, 'Confidential', 'should delete asap', 'PTH7vmTajr'))
cur.execute("INSERT INTO notes (locked, title, subtitle, message) VALUES (?,?,?,?)", (0, 'TODO', 'kinda urgent', 'To Do: research \'SQL Injection\', \'XSS\', \'Path Traversal\''))
cur.execute("INSERT INTO notes (locked, title, subtitle, message) VALUES (?,?,?,?)", (0, 'TODO', 'important', 'To Do: Study for IT Security in Large IT Infrastructures Exam'))
cur.execute("INSERT INTO notes (locked, title, subtitle, message) VALUES (?,?,?,?)", (0, 'TODO', 'important', 'To Do: Study for Security for Systems Engineering Exam'))
cur.execute("INSERT INTO notes (locked, title, message) VALUES (?,?,?)", (0, 'Note' , 'Note: check out streaming service (i think?) called NETTERmusic'))
cur.execute("INSERT INTO notes (locked, title, message) VALUES (?,?,?)", (0, 'Note', 'My First Note'))
cur.execute("INSERT INTO notes (locked, title, subtitle, message, note_password) VALUES (?,?,?,?,?)", (1, 'TODO', 'very urgent', 'I think my notes app is not completely secure. To Do: check for vulnerabilities', '3pVDvMUJSw'))
cur.execute("INSERT INTO notes (locked, title, subtitle, message, note_password) VALUES (?,?,?,?,?)", (1, 'Note', 'private', 'My First Secret Note', 'XRndd25Xhd'))
cur.execute("INSERT INTO notes (locked, title, message, note_password) VALUES (?,?,?,?)", (1, 'Confidential', 'Password for Mail: supersecretpassword123', '4Lvs2BnhXV'))


connection.commit()
connection.close()
