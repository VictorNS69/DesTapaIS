# IS2-2019-2020
Repositorio del Grupo 01 de la asignatura de Ingeniería del Software 2 para la práctica de la asignatura

## Requisitos
- Python 3.7
- SQLite3
## Pasos para ejecutar la aplicación
### 1. Crear el entorno virtual
Para crear el entorno virtual, necesitarás tener instalado `virtualenv wrapper`. En el siguiente [gist](https://gist.github.com/VictorNS69/25f82339708714628177a7e2bd566afc) tendrás información de cómo hacerlo.

Crear un entorno virtual con **Python3.7** llamado _DesTapaIS_.
```bash
mkvirtualenv --python=/usr/bin/python3.7 DesTapaIS
```
Si el entorno no se ha activado por defecto, activalo.
```bash
workon DesTapaIS
```
Una vez creado, instalar las dependencias:
```bash
pip install -r requirements.txt
```
### 2. Generar una base de datos vacía
Desde la carpeta raiz ejecutar la siguiente llamada.
```bash
./src/scripts/script_db.py
```
### 3. Ejecutar la aplicación
Tan solo corre el archivo `run_app.sh` desde la carpeta raiz:
```bash
./run_app.sh
```
## Autores
- [Víctor Nieves](https://github.com/VictorNS69)
- [Daniel Morgera](https://github.com/dmorgera)
- [Andrea Velarde](https://github.com/AndreaVentur10)
- [Yanran Chen](https://github.com/YanranCW)
- [Alejandro Senovilla](https://github.com/Alexsente)
## Licencia
[GNU General Public License v3.0](LICENSE)
