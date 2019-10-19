#!/usr/bin/python3

import sqlite3
import os

if os.path.exists("../DesTapaIS.db"):
    os.remove("../DesTapaIS.db")
    print("La base de datos (DB) ha sido borrada con exito")

conn = sqlite3.connect('../DesTapaIS.db')
c = conn.cursor()

""" 
Esta linea se debe escribir por cada conexion para tener en cuenta las 
FOREIGN KEYs.
"""
c.execute('''PRAGMA foreign_keys = ON;''')

c.execute('''CREATE TABLE Usuario
             (id INTEGER PRIMARY KEY,
             username TEXT NOT NULL UNIQUE,
             contrasena TEXT NOT NULL, 
             email TEXT NOT NULL UNIQUE, 
             fecha_nacimiento DATE NOT NULL, 
             nombre TEXT, 
             apellidos TEXT,
             pais TEXT, 
             foto BLOB, 
             descripcion TEXT, 
             genero TEXT, 
             verificado INTEGER DEFAULT 0 NOT NULL);''')

c.execute('''CREATE TABLE Amistad
             (Usuario_id INTEGER,
             Usuario_id1 INTEGER, 
             fecha DATE NOT NULL,
             aprobado INTEGER DEFAULT 0 NOT NULL,
             FOREIGN KEY(Usuario_id) REFERENCES Usuario(id),
             FOREIGN KEY(Usuario_id1) REFERENCES Usuario(id));''')

c.execute('''CREATE TABLE Galardon
             (id INTEGER PRIMARY KEY,
             nombre TEXT, 
             tipo TEXT,
             nivel INTEGER, 
             imagen BLOB,
             condiciones TEXT)''')

c.execute('''CREATE TABLE Obtiene_galardon
             (Usuario_id INTEGER NOT NULL,
             Galardon_id INTEGER NOT NULL,
             fecha DATE NOT NULL, 
             FOREIGN KEY(Usuario_id) REFERENCES Usuario (id),
             FOREIGN KEY(Galardon_id) REFERENCES Galardon (id))''')

c.execute('''CREATE TABLE Local
             (id INTEGER PRIMARY KEY,
             nombre TEXT, 
             direccion TEXT, 
             resena TEXT, 
             Usuario_id INTEGER,
             FOREIGN KEY(Usuario_id) REFERENCES Usuario (id))''')

c.execute('''CREATE TABLE Favorito_local
             (Usuario_id INTEGER NOT NULL,
             Local_id INTEGER NOT NULL,
             fecha DATE NOT NULL, 
             FOREIGN KEY(Usuario_id) REFERENCES Usuario (id),
             FOREIGN KEY(Local_id) REFERENCES Local (id))''')

c.execute('''CREATE TABLE Degustacion
             (id INTEGER PRIMARY KEY,
             valoracion_promedio DOUBLE NOT NULL,
             nombre TEXT NOT NULL, 
             descripcion TEXT NOT NULL UNIQUE, 
             fecha DATE NOT NULL, 
             tipo_comida TEXT NOT NULL, 
             procedencia TEXT NOT NULL,
             tamaño TEXT NOT NULL, 
             foto BLOB NOT NULL, 
             calificador_gusto TEXT NOT NULL, 
             Usuario_id INTEGER, 
             Local_id INTEGER,
             FOREIGN KEY (Usuario_id) REFERENCES Usuario (id),
             FOREIGN KEY (Local_id) REFERENCES Local (id))''')

c.execute('''CREATE TABLE Favorito_degustacion
             (Usuario_id INTEGER NOT NULL,
             Degustacion_id INTEGER NOT NULL,
             fecha DATE NOT NULL, 
             FOREIGN KEY(Usuario_id) REFERENCES Usuario (id),
             FOREIGN KEY(Degustacion_id) REFERENCES Degustacion (id))''')

c.execute('''CREATE TABLE Valoracion
             (Usuario_id INTEGER NOT NULL,
             Degustacion_id INTEGER NOT NULL,
             valor INTEGER NOT NULL, 
             FOREIGN KEY(Usuario_id) REFERENCES Usuario (id),
             FOREIGN KEY(Degustacion_id) REFERENCES Degustacion (id))''')

conn.commit()

conn.close()

print("Se ha creado la nueva base de datos (DB) vacia.")
