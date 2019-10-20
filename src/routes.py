from src import app, DB_PATH

from flask import render_template, request
import sqlite3


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        # print("SE HA PULSADO EL BOTÓN")
        with sqlite3.connect(DB_PATH) as conn:
            # print("ME HE CONECATDO A LA DB")
            c = conn.cursor()
            c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
            details = request.form
            # print("SE HA HECHO EL REQUEST.FORM", details)
            # TODO: Hashear lar contraseña
            # TODO: Desde el HTML (con JS?) hacer que las contraseñas sean iguales
            # TODO: Añadir todos los valores
            query = "INSERT INTO Usuario(username, contrasena, email, fecha_nacimiento) VALUES ('{}', '{}', '{}', '12-12-2999');"\
                .format(details["username"], details["password"], details["email"])
            print("Query:\t", str(query))  # -- Por terminal
            try:
                c.execute(str(query))
                conn.commit()
                print("Añadido a la DB")
            except sqlite3.IntegrityError:
                print("El usuario ya existe o datos invalidos")
            except sqlite3.OperationalError:
                print("DB bloqueada")

        return 'success post'
    return render_template('sign_up.html')
