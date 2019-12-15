import sqlite3, datetime, base64
from src import app, DB_PATH, functions, exceptions
from flask import render_template, request, redirect, url_for, json
from werkzeug.security import generate_password_hash, check_password_hash
from base64 import b64encode


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
                if result is None:
                    return render_template("user_not_exist.html")

                if result[-1] == 0:
                    return render_template("no_verification.html", username=details["username"])

                check = check_password_hash(result[2], details["password"])
                if check:
                    return redirect(url_for('homepage', username=details["username"]))
                else:
                    return render_template("wrong_pw.html")

            except sqlite3.IntegrityError as e:
                return e  # render_template('error_sign_in.html', name=details["username"], email=details["email"])
            except sqlite3.OperationalError as e:
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
                verified = 0

                query = "INSERT INTO 'Usuario' ('username', 'contrasena', 'email', 'fecha_nacimiento', nombre," \
                        "'apellidos', 'pais', 'descripcion', 'genero', 'verificado', 'foto') VALUES (?, ?, ?, ?, ?, " \
                        "?, ? , ?, ?, ?, ?)"
                data_tuple = (details["username"], generate_password_hash(details["password"]), details["email"],
                              str(details["date"]), details["firstname"], details["lastname"], details["country"],
                              details["description"], details["sex"], verified, blob)
                try:
                    c.execute(query, data_tuple)
                    conn.commit()
                    from_address = "destapais.grupo1@gmail.com"
                    to_address = details["email"]
                    subject = "DesTapaIS verification mail"
                    message = "Hi! "+details["username"]+" This is your verification link: " \
                              "http://127.0.0.1:5000/"+details["username"]+"/verification"
                    username = "destapais.grupo1"
                    psw = "grupo1IS2"

                    functions.send_email(from_address, [to_address], "", subject, message, username, psw)

                    return render_template('verify_yourself.html', username=details["username"])

                except sqlite3.IntegrityError as e:
                    return render_template('error_sign_in.html', name=details["username"], email=details["email"])
                except sqlite3.OperationalError as e:
                    return "Error 503 Service Unavailable.\nPlease try again later"

    return render_template('sign_up.html')


@app.route('/<string:username>/profile', methods=['GET', 'POST'])
def profile(username):
    try:
        functions.verified_user(DB_PATH, username)
    except exceptions.UserNotExist:
        return render_template("user_not_exist.html")

    except exceptions.UserNOtVerified:
        return render_template("no_verification.html", username=username)

    if request.method == "POST":
        return redirect(url_for('edit_info', username=username))
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
            query = "SELECT * FROM Usuario WHERE username = ? "
            c.execute(query, (username,))
            conn.commit()
            result = c.fetchone()
            image = b64encode(result[-4]).decode("utf-8")

    except sqlite3.OperationalError as e:
        return "Error 503 Service Unavailable.\nPlease try again later"

    return render_template('userprofile.html', username=username, result=result, image=image)


@app.route('/<string:username>/home')
def homepage(username):
    try:
        functions.verified_user(DB_PATH, username)
    except exceptions.UserNotExist:
        return render_template("user_not_exist.html")

    except exceptions.UserNOtVerified:
        return render_template("no_verification.html", username=username)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        query = "SELECT * FROM Usuario WHERE username = ? "
        c.execute(query, (username,))
        conn.commit()
        result = c.fetchone()
        image = b64encode(result[-4]).decode("utf-8")
        query = "SELECT * FROM Degustacion INNER JOIN Valoracion ON Valoracion.Degustacion_id=Degustacion.id " \
                "ORDER BY Valoracion.valor LIMIT 4"
        c.execute(query)
        degustaciones = c.fetchall()
        query = "SELECT * FROM Degustacion INNER JOIN Valoracion ON Valoracion.Degustacion_id=Degustacion.id " \
                "ORDER BY Valoracion.valor DESC LIMIT 4"
        c.execute(query)
        mvtastings = c.fetchall()
        query = "SELECT * FROM Local LIMIT 4"
        c.execute(query)
        locals = c.fetchall()
    return render_template('homepage.html', username=username, user=(result, image), tastings=degustaciones,
                           most_valued_tastings=mvtastings, locals=locals)


@app.route('/<string:username>/new_local',  methods=['GET', 'POST'])
def new_local(username):
    try:
        functions.verified_user(DB_PATH, username)
    except exceptions.UserNotExist:
        return render_template("user_not_exist.html")

    except exceptions.UserNOtVerified:
        return render_template("no_verification.html", username=username)

    if request.method == "POST":
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
            details = request.form
            query = "SELECT id FROM Usuario WHERE username='{}'".format(username)
            c.execute(query)
            id_user = c.fetchone()[0]
            query = "INSERT INTO Local (nombre, direccion, resena, Usuario_id) VALUES (?, ?, ?, ?)"
            data_tuple = (details["name"], details["address"], details["description"], id_user)
            try:
                c.execute(query, data_tuple)
                conn.commit()
                return redirect(url_for('new_tasting', username=username))
            except sqlite3.IntegrityError as e:
                return render_template('local_already_exists.html', username=username)

    return render_template('new_local.html', username=username)


@app.route('/<username>/friends', methods=['GET', 'POST'])
def amigos(username):
    try:
        functions.verified_user(DB_PATH, username)
    except exceptions.UserNotExist:
        return render_template("user_not_exist.html")

    except exceptions.UserNOtVerified:
        return render_template("no_verification.html", username=username)

    return render_template('friends.html')


@app.route('/<string:username>/new_tasting', methods=['GET', 'POST'])
def new_tasting(username):
    try:
        functions.verified_user(DB_PATH, username)
    except exceptions.UserNotExist:
        return render_template("user_not_exist.html")

    except exceptions.UserNOtVerified:
        return render_template("no_verification.html", username=username)

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
    if request.method == 'POST':
            c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
            details = request.form
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
            suma = 0
            for valor in valores:
                suma += valor[0]
            valor_promedio = suma / len(valores)
            query = "UPDATE 'Degustacion' SET 'valoracion_promedio'='{}'".format(valor_promedio)
            c.execute(query)
            conn.commit()
            return render_template('ok_tasting.html', username=username)

    query = "SELECT nombre FROM Local"
    c.execute(query)
    locales_tupla = c.fetchall()
    locales = []
    for local in locales_tupla:
        locales.append(local[0])
    return render_template('new_tasting.html', username=username, locales=locales)

  
@app.route('/<username>/tastings/<id_tasting>', methods=['GET', 'POST'])
def tasting(username, id_tasting):
    try:
        functions.verified_user(DB_PATH, username)
    except exceptions.UserNotExist:
        return render_template("user_not_exist.html")

    except exceptions.UserNOtVerified:
        return render_template("no_verification.html", username=username)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            if request.method == 'POST':
                query = "SELECT id FROM Usuario WHERE username = ? "
                c.execute(query, (username,))
                conn.commit()
                id_user = c.fetchone()[0]
                query = "INSERT INTO 'Favorito_degustacion' ('Usuario_id', 'Degustacion_id', 'fecha') VALUES (?, ?, ?)"
                data_tuple = (id_user, id_tasting, str(datetime.datetime.now()))
                c.execute(query, data_tuple)
                conn.commit()
                return redirect(url_for('homepage', username=username))
            c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
            query = "SELECT * FROM Degustacion WHERE id = ? "
            c.execute(query, (id_tasting,))
            conn.commit()
            result = c.fetchone()
            query = "SELECT nombre FROM Local WHERE id = ?"
            c.execute(query, (result["Local_id"],))
            local = c.fetchone()[0]
            image= base64.b64encode(result["foto"]).decode("utf-8")

    except sqlite3.OperationalError as e:
        return "Error 503 Service Unavailable.\nPlease try again later"
    return render_template('tasting.html', result=result, image=image, local=local, username=username)


@app.route('/<username>/locals/<id_local>', methods=['GET', 'POST'])
def local(username, id_local):
    try:
        functions.verified_user(DB_PATH, username)
    except exceptions.UserNotExist:
        return render_template("user_not_exist.html")

    except exceptions.UserNOtVerified:
        return render_template("no_verification.html", username=username)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
        if request.method == 'POST':
            query = "SELECT id FROM Usuario WHERE username = ? "
            c.execute(query, (username,))
            conn.commit()
            id_user = c.fetchone()[0]
            query = "INSERT INTO 'Favorito_local' ('Usuario_id', 'Local_id', 'fecha') VALUES (?, ?, ?)"
            data_tuple = (id_user, id_local, str(datetime.datetime.now()))
            c.execute(query, data_tuple)
            conn.commit()
            return redirect(url_for('homepage', username=username))
        c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
        query = "SELECT * FROM Local WHERE id = ? "
        c.execute(query, (id_local,))
        conn.commit()
        result = c.fetchone()
    except sqlite3.OperationalError as e:
        return "Error 503 Service Unavailable.\nPlease try again later"
    return render_template('local.html', username=username, result=result)

  
@app.route('/<string:username>/search', methods=['GET', 'POST'])
def search(username):
    try:
        functions.verified_user(DB_PATH, username)
    except exceptions.UserNotExist:
        return render_template("user_not_exist.html")

    except exceptions.UserNOtVerified:
        return render_template("no_verification.html", username=username)

    if request.method == 'POST':
        return redirect(url_for('search_list', username=username, request=json.dumps(request.form)))
    return render_template('search.html', username=username)


@app.route('/<string:username>/search_list/<request>', methods=['GET', 'POST'])
def search_list(username, request):
    try:
        functions.verified_user(DB_PATH, username)
    except exceptions.UserNotExist:
        return render_template("user_not_exist.html")

    except exceptions.UserNOtVerified:
        return render_template("no_verification.html", username=username)

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        req = json.loads(request)
        if req["category"] == "None":
            return render_template('select_category.html', username=username)

        regex = req["text"]
        if req["category"] == "Usuario":
            query = "SELECT * FROM Usuario WHERE username LIKE '%" + regex + "%' OR email LIKE '%" + regex +\
                    "%' OR nombre LIKE '%" + regex + "%' OR apellidos LIKE '%" + regex + \
                    "%' OR pais LIKE '%" + regex + "%' OR descripcion LIKE '%" + regex \
                    + "%' EXCEPT SELECT * FROM Usuario WHERE username='{}';".format(username)
        elif req["category"] == "Local":
            query = "SELECT * FROM Local WHERE nombre LIKE '%" + regex + "%' OR direccion LIKE '%" + regex + \
                    "%' OR resena LIKE '%" + regex + "%';"
        elif req["category"] == "Degustacion":
            query = "SELECT * FROM Degustacion WHERE nombre LIKE '%" + regex + "%' OR descripcion LIKE '%" + regex +\
                "%' OR tipo_comida LIKE '%" + regex + "%' OR procedencia LIKE '%" + regex +\
                "%' OR valoracion_promedio LIKE '%" + regex + "%' OR calificador_gusto LIKE '%" + regex + "%';"

        c.execute(query)
        values = c.fetchall()
        if not values:
            return render_template('search_no_results.html', username=username)

        return render_template('search_list.html', username=username, request=(req["category"], values))


@app.route('/<string:username>/help', methods=['GET', 'POST'])
def help(username):
    try:
        functions.verified_user(DB_PATH, username)
    except exceptions.UserNotExist:
        return render_template("user_not_exist.html")

    except exceptions.UserNOtVerified:
        return render_template("no_verification.html", username=username)

    if request.method == 'POST':
        return render_template('thank_you.html', username=username)

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        query = "SELECT * FROM Usuario WHERE username='{}';".format(username)
        c.execute(query)
        value = c.fetchone()
        return render_template('bug&comments.html', username=username, email=value[3])


@app.route('/<string:username>/verification', methods=['GET', 'POST'])
def verification(username):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        query = "UPDATE Usuario SET verificado=1 WHERE username='{}';".format(username)
        c.execute(query)
        c.fetchone()
    return redirect(url_for('login', username=username))


@app.route('/<string:username>/most_valued_tastings', methods=['GET'])
def most_valued_tastings(username):
    try:
        functions.verified_user(DB_PATH, username)
    except exceptions.UserNotExist:
        return render_template("user_not_exist.html")

    except exceptions.UserNOtVerified:
        return render_template("no_verification.html", username=username)

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        query = "SELECT * FROM Degustacion INNER JOIN Valoracion ON Valoracion.Degustacion_id=Degustacion.id " \
                "ORDER BY Valoracion.valor DESC"
        c.execute(query)
        degustaciones = c.fetchall()
        images = []
        [images.append(b64encode(d[-7]).decode("utf-8") if d[-7] else None) for d in degustaciones]
        return render_template('most_valued_tastings.html', username=username, degustaciones=degustaciones, foto=images)


# Error definition
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404_error_page.html')


@app.errorhandler(Exception)
def exception_handler(error):
    print(error)
    return render_template('something_broke.html')
