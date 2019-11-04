from src import app, DB_PATH, functions
from flask import render_template, request
import sqlite3


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('init.html')


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
                data_tuple = (details["username"], hash(details["password"]), details["email"], str(details["date"]),
                              details["firstname"], details["lastname"], details["country"], details["description"],
                              details["sex"], verified, blob)
                try:
                    c.execute(query, data_tuple)
                    conn.commit()
                    conn.close()
                    # TODO: return HTML mira tu correo para validar
                    # TODO: return HTML menú principal ha de ser la ruta /login
                    render_template('login.html')
                except sqlite3.IntegrityError as e:
                    print("Error:", e)
                    return render_template('error_sign_in.html', name=details["username"], email=details["email"])
                except sqlite3.OperationalError as e:
                    print("Error:", e)
                    return "Error 503 Service Unavailable.\nPlease try again later"

    return render_template('sign_up.html')


@app.route('/<string:username>/homepage/resume', methods=['GET'])
def resume(username):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
            query = "SELECT * FROM Usuario WHERE username = ? "
            c.execute(query, (username,))
            conn.commit()
            result = c.fetchone()

    except sqlite3.OperationalError as e:
        print("Error:", e)
        return "Error 503 Service Unavailable.\nPlease try again later"

    return render_template('resume.html', result=result)


@app.route('/<string:username>/homepage')
def homepage(username):
    return render_template('homepage.html',username=username)



@app.route('/<string:username>/homepage/profile', methods=['GET'])
def profile(username):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
            query = "SELECT * FROM Usuario WHERE username = ? "
            c.execute(query, (username,))
            conn.commit()
            result = c.fetchone()

    except sqlite3.OperationalError as e:
        print("Error:", e)
        return "Error 503 Service Unavailable.\nPlease try again later"

    return render_template('profile.html', result=result)