import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['key'] = 'random string'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('''PRAGMA synchronous = OFF''')
    return conn, cur


@app.route('/')
def index():
    conn, cur = get_db_connection()

    notes = cur.execute('SELECT * FROM notes WHERE locked = 0 ORDER BY created DESC').fetchall()
    lockednotes = cur.execute('SELECT title, created, note_password FROM notes WHERE locked = 1 ORDER BY created DESC').fetchall()
    conn.close()

    return render_template('index.html', notes=notes, lockednotes=lockednotes)


@app.route('/locked')
def locked():
    notes = []
    entries = []
    my_password_hashed= ""

    title = request.args.get("title") if "title" in request.args else None
    password = request.args.get("password") if "password" in request.args else None

    if password and title:
        try:
            conn, cur = get_db_connection()
            entries = cur.execute("SELECT * FROM notes WHERE title = ?", (title,)).fetchall()
            conn.close()

            for entry in entries:
                my_password_hashed = entry['note_password']

                if password == my_password_hashed:
                    notes.append(entry)
                else:
                    my_password_provided = eval(password)
                    if my_password_provided == my_password_hashed:
                        notes.append(entry)
        except:
            print("Nope. Try again.")

    return render_template('locked.html', notes=notes)


@app.route('/search/', methods=('GET', 'POST'))
def search():
    conn, cur = get_db_connection()
    notes = []

    notes = cur.execute('SELECT * FROM notes WHERE locked = 0').fetchall()

    if request.method == 'POST':
        search = request.form['search']
        if search:
            notes = cur.execute("SELECT * FROM notes WHERE locked = 0 AND title LIKE ? OR message LIKE ?", ('%' + search + '%','%' + search + '%',)).fetchall()
            conn.close()
        else:
            notes = cur.execute('SELECT * FROM notes WHERE locked = 0').fetchall()
            conn.close()

    return render_template('search.html', notes=notes)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    conn, cur = get_db_connection()

    if request.method == 'POST':
        if not 'message' in request.form:
            return render_template('create.html')
            
        message = request.form['message']
        note_password = ""

        if 'title' in request.form:
            title = request.form['title']
        else:
            title = "Note"

        if 'subtitle' in request.form:
            subtitle = request.form['subtitle']
        else:
            subtitle = ""

        if 'locked' in request.form:
            locked = "1"
            if 'note_password' in request.form:
                note_password = request.form['note_password']
        else:
            locked = "0"
            note_password = ""
            
        cur.execute('INSERT INTO notes (locked, title, subtitle, message, note_password) VALUES (?,?,?,?,?)', (locked, title, subtitle, message, note_password,))
        conn.commit()
        conn.close()

    return render_template('create.html')
