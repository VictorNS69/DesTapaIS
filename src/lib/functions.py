import datetime
import smtplib
import sqlite3
from . import exceptions as E


def date_validator(date):
    """ Valida si la fecha introducida es mayor de edad (mayor de 18 años)

    :param date: fecha en formato YYYY-MM-DD
    :return: True si es mayor de edad, False si no
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    d2 = datetime.datetime.strptime(today, "%Y-%m-%d")
    d1 = datetime.datetime.strptime(date, "%Y-%m-%d")
    sub = abs((d1 - d2).days)
    return False if d1 > d2 or sub < 365*18 else True


def send_email(from_address, to_address, cc_address,
               subject, msg, username, psw, smtp_server='smtp.gmail.com:587'):
    """Function that creates the email and sends it.
    :param:from_address: from address.
    :param: to_address: to address. Must be a list
    :param: cc_address: cc address.
    :param: subject: subject.
    :param: msg: message.
    :param: username: username.
    :param: psw: password.
    :param: smtp_server: smtpserver.
    :return: """

    header = 'From: %s\n'%from_address
    header += 'To: %s\n'%','.join(to_address)
    header += 'Cc: %s\n'%','.join(cc_address)
    header += 'Subject: %s\n\n'%subject
    msg = header + msg

    server = smtplib.SMTP(smtp_server)
    server.starttls()
    server.login(username, psw)
    problems = server.sendmail(from_address, to_address, msg)
    server.quit()
    return problems


def verified_user(db_path, username):
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute('''PRAGMA foreign_keys = ON;''')  # Parece que no es necesaria esta linea
        query = "SELECT * FROM Usuario WHERE username='{}'".format(username)
        try:
            c.execute(query)
            result = c.fetchone()
            if result is None:
                raise E.UserNotExist()

            if result[-1] == 0:
                raise E.UserNOtVerified()
        except sqlite3.IntegrityError as e:
            return e
        except sqlite3.OperationalError as e:
            return e
