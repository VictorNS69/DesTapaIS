from src import app, DB_PATH, functions
from flask import render_template, request
import sqlite3


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == "POST":
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
            details = request.form
            # TODO: Añadir todos los valores
            date = functions.date_validator(str(details["date"]).replace("/", "-"))
            if not date:
                print("Edad mal")
                return render_template('age_error.html')
            else:
                print("edad-- ", date)
                print("Edad bien")

                query = "INSERT INTO Usuario(username, contrasena, email, fecha_nacimiento) " \
                        "VALUES ('{}', '{}', '{}', '{}');"\
                    .format(details["username"], hash(details["password"]), details["email"], str(details["date"]))
                print("Query:\t", str(query))
                try:
                    c.execute(str(query))
                    conn.commit()
                    print("Añadido a la DB")
                    # TODO: return HTML mira tu correo para validar
                    # TODO: return HTML menú principal
                    return "success"
                except sqlite3.IntegrityError:
                    return render_template('error_sign_in.html', name=details["username"], email=details["email"])
                except sqlite3.OperationalError:
                    print("DB bloqueada")
                    return "Error 503 Service Unavailable.\nPlease try again later"

    return render_template('sign_up.html')

