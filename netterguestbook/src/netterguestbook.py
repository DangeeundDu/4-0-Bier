from importlib.resources import path
from flask import Flask, jsonify, request, abort, request, render_template, redirect, send_file, send_from_directory
import json
import os
import sqlite3
from sqlite3 import OperationalError
import random
import hashlib
from werkzeug.utils import secure_filename
import urllib.parse
import uuid
import datetime
import pathlib
import tempfile
import io

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = "uploads"
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 ** 2

# mechanism to make SQL-injection impossible
secret = open("secret").read()


def compute_security_hash(value):
    # todo: md5 is deprecated, maybe use hmac in future version?
    return hashlib.md5((secret + value).encode()).hexdigest()


@app.route('/execute_query/<sqlite_query>', methods=['GET'])
def execute_query(sqlite_query):
    verify = request.args.get("verify")
    send_pdf = "pdf" in request.args

    if verify != compute_security_hash(sqlite_query):
        abort(401)

    try:
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute('''PRAGMA synchronous = OFF''')
        cur.execute(sqlite_query)
        result = cur.fetchall()

        if send_pdf:
            with tempfile.NamedTemporaryFile() as f:
                f.write(render_template('printout.tex', data=result).encode())
                f.flush()
                basename = pathlib.Path(f.name).name
                os.system(f"cd /tmp; pdflatex {f.name}")
                with open(f"{f.name}.pdf", "rb") as pdf_file:
                    pdf_data = pdf_file.read()
                    os.system(f"rm -f /tmp/{basename}.*")
                return send_file(io.BytesIO(pdf_data), attachment_filename="printout.pdf")

        return jsonify(result)
    except OperationalError:
        abort(402)


@app.route('/')
def index():
    secret = hashlib.md5(request.args.get("secret").encode()).hexdigest() if "secret" in request.args else None

    if secret:
        # prevent sql injections (blacklisting insecure terms)
        secret = secret.replace("1 = 1", "").replace("OR TRUE", "")
        sql_query = "SELECT * FROM post WHERE is_public = 0 AND secret = \"" + secret + "\""
    else:
        sql_query = "SELECT * FROM post WHERE is_public = 1"

    verify = compute_security_hash(sql_query)

    if "only_signed_url" in request.args:
        return f"/execute_query/{urllib.parse.quote(sql_query)}?verify={urllib.parse.quote(verify)}"
    else:
        body_class = "secret" if "secret" in request.args else "public"
        return render_template('index.html', body_class=body_class, sql_query=sql_query, verify=verify)


@app.route('/upload')
def upload_page():
    return render_template('upload.html')


@app.route('/download')
def download():
    filename = request.args.get("filename")
    return send_from_directory("uploads", filename)


def used_space_in_megabytes():
    return sum(f.stat().st_size for f in pathlib.Path("./uploads/").glob('*') if f.is_file()) // (1024 ** 2)


@app.route('/post', methods=['POST'])
def create_post():
    if request.method == 'POST':
        date = datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")
        is_public = request.form.get("is_public")
        if not is_public in ["0", "1"]:
            abort(400)

        secret = request.form.get("secret")
        if secret:
            secret = hashlib.md5(secret.encode()).hexdigest()

        message = request.form.get("message")

        if "file" in request.files and request.files["file"].filename != "":
            uploaded_file = request.files['file']
            filename = str(uuid.uuid4())
            filepath = "./uploads/{}".format(filename)

            while used_space_in_megabytes() > 128:
                oldest_file = min(pathlib.Path("./uploads/").glob('*'), key=os.path.getctime)
                os.remove(oldest_file)

            uploaded_file.save(filepath)

        else:
            filename = None

        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute('''PRAGMA synchronous = OFF''')
        cur.execute("INSERT INTO post (date, is_public, secret, message, image_path) VALUES (?, ?, ?, ?, ?)",
                    (date, is_public, secret, message, filename))
        con.commit()
        con.close()
        return render_template('direct_to_root.html')


if __name__ == '__main__':
    app.run()
