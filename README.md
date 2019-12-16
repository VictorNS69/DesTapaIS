# DesTapaIS
Repositorio del Grupo 01 de la asignatura de Ingeniería del Software 2 para la práctica de la asignatura
## Abstract
**_Descubre Tapas by ISII_** (_DesTapaIS_) es una nueva forma de compartir socialmente y explorar el mundo de los
restaurantes y bares con tus amigos y el resto del mundo. Con esta aplicación
queremos saber que están saboreando o que se come de manera más típico en una
zona. Además se podrán calificar los vinos, cocteles. Puede entrar en los perfiles de
tus amigos y realizar comentarios sobre la comida o el sitio. Además, el sistema
_DesTapaIS_ te podrá realizar recomendaciones basadas en lo que os ha ido gustando
a ti y a tus amigos. Como funcionalidad para motivar, _DesTapaIS_ te permite obtener
galardones por completar actividades gastronómicas.

Para más información, consulta el [enunciado](/documentacion/enunciado.pdf) de la práctica.

### Nota
**No se ha implementado toda la funcionalidad que propone el enunciado**. El objetivo principal de esta práctica era el poder manejar un proyecto "de verdad", elaborando los documentos pertinentes y planificando y dejando constancia de todo.

## Releases
En el apartado de [_releases_](https://github.com/VictorNS69/ISII-2019-2020/releases) podrás encontrar cada una de las versiones que ha tenido estre proyecto a lo largo de su desarrollo. Además, podrás encontrar en ellas la documentación de cada entrega, y las presentaciones que se han realizado.
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
