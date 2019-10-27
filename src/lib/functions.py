import datetime


def date_validator(date):
    """ Valida si la fecha introducida es mayor de edad (mayor de 18 años)

    :param date: fecha en formato YYYY-MM-DD
    :return: True si es mayor de edad, False si no
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    d2 = datetime.datetime.strptime(today, "%Y-%m-%d")
    d1 = datetime.datetime.strptime(date, "%Y-%m-%d")
    sub = abs((d1 - d2).days)
    return False if d1 > d2 or sub < 365*8 else True
