import sqlite3
from src import app, DB_PATH, functions
from flask import render_template, request, redirect, url_for, json
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

@app.route('/<string:username>/new_tasting', methods=['GET', 'POST'])
def new_tasting(username):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
    if request.method == 'POST':
            c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
            details = request.form
            print(details)
            image = request.files["image"]
            blob = image.read()
            query = "SELECT nombre, Local_id FROM Degustacion"
            c.execute(query)
            tuplas = c.fetchall()
            query = "SELECT id FROM Local WHERE nombre='{}'".format(details["local"])
            c.execute(query)
            id_local = c.fetchone()[0]
            for tupla in tuplas:
                if (tupla[0] == details["name"]) and (tupla[1] == id_local):
                    return render_template('deg_already_exists.html', username=username)
            query = "SELECT id FROM Usuario WHERE username='{}'".format(username)
            c.execute(query)
            id_user = c.fetchone()[0]
            query = "INSERT INTO 'Degustacion' ('valoracion_promedio', 'nombre', 'descripcion', 'fecha'," \
                    "'tipo_comida', 'procedencia', 'tamaño', 'foto', 'calificador_gusto', 'Usuario_id'," \
                    "'Local_id')" \
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, (SELECT id FROM Usuario WHERE nombre='{}'), "\
                    + str(id_local) + ")".format(username)
            data_tuple = (0, details["name"], details["description"], details["date"], details["type"],
                          details["origin"], details["size"], blob, details["taste"])
            c.execute(query, data_tuple)
            conn.commit()
            query = "SELECT id FROM Degustacion WHERE nombre='{}'".format(details["name"])
            c.execute(query)
            id_deg = c.fetchone()[0]
            query = "INSERT INTO 'Valoracion' ('Usuario_id', 'Degustacion_id', 'valor') VALUES (?, ?, ?)"
            data_tuple = (id_user, id_deg, details["rate"])
            c.execute(query, data_tuple)
            conn.commit()
            query = "SELECT valor FROM Valoracion WHERE Degustacion_id='{}'".format(id_deg)
            c.execute(query)
            valores = c.fetchall()
            print(valores)
            suma = 0
            for valor in valores:
                suma += valor[0]
                print("suma:"+str(suma))
            valor_promedio = suma / len(valores)
            print("valor promedio: "+str(valor_promedio))
            query = "UPDATE 'Degustacion' SET 'valoracion_promedio'='{}'".format(valor_promedio)
            c.execute(query)
            conn.commit()

    query = "SELECT nombre FROM Local"
    c.execute(query)
    locales_tupla = c.fetchall()
    locales = []
    for local in locales_tupla:
        locales.append(local[0])
    return render_template('new_tasting.html', username=username, locales=locales)




