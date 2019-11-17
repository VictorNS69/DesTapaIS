import sqlite3
from src import app, DB_PATH, functions
from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/', methods=['GET', 'POST'])
def init():
    return render_template('init.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
            details = request.form
            query = "SELECT * FROM Usuario WHERE username='{}'".format(details["username"])
            try:
                c.execute(query)
                result = c.fetchone()
                print("result", result)
                if result is None:
                    return render_template("user_not_exist.html")
                check = check_password_hash(result[2], details["password"])
                if check:
                    return redirect(url_for('homepage', username=details["username"]))
                else:
                    return render_template("wrong_pw.html")

            except sqlite3.IntegrityError as e:
                print("Error:", e)
                return e  # render_template('error_sign_in.html', name=details["username"], email=details["email"])
            except sqlite3.OperationalError as e:
                print("Error:", e)
                return e  # "Error 503 Service Unavailable.\nPlease try again later"

    return render_template('login.html')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == "POST":
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
            details = request.form
            date = functions.date_validator(str(details["date"]).replace("/", "-"))
            if not date:
                return render_template('age_error.html')
            else:
                image = request.files["image"]
                blob = image.read()
                verified = 1  # TODO: elimiar verificado hardcoded cuando se tenga verificacion por correo

                query = "INSERT INTO 'Usuario' ('username', 'contrasena', 'email', 'fecha_nacimiento', nombre," \
                        "'apellidos', 'pais', 'descripcion', 'genero', 'verificado', 'foto') VALUES (?, ?, ?, ?, ?, " \
                        "?, ? , ?, ?, ?, ?)"
                data_tuple = (details["username"], generate_password_hash(details["password"]), details["email"],
                              str(details["date"]), details["firstname"], details["lastname"], details["country"],
                              details["description"], details["sex"], verified, blob)
                try:
                    c.execute(query, data_tuple)
                    conn.commit()
                    # TODO: return HTML mira tu correo para validar
                    return redirect(url_for('homepage', username=details["username"]))
                except sqlite3.IntegrityError as e:
                    print("Error:", e)
                    return render_template('error_sign_in.html', name=details["username"], email=details["email"])
                except sqlite3.OperationalError as e:
                    print("Error:", e)
                    return "Error 503 Service Unavailable.\nPlease try again later"

    return render_template('sign_up.html')


@app.route('/<string:username>/home')
def homepage(username):
    return render_template('homepage.html', username=username)


@app.route('/<username>/friends', methods=['GET', 'POST'])
def amigos(username):
    return render_template('friends.html')

