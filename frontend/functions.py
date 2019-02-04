from datetime import datetime
from bitmath import Byte, Bit, SI

# funkce pro hezčí zobrazování parametrů, každá funkce musí být deklarována
# v souboru app.py, tak aby na ni šlo dosáhnout i z templatů (jinja2)


def niceDate(string, form='long'):
    """ převede string na české datum
        když je form long, tak vrátí i s časem, když short, tak pouze datum
        pokud je ve formátu na konci Z, tak ho odstraní
        'NA' je defaultní hodnota pro nevyplněné pole
    """
    if string == 'NA':
        return 'NA'

    if string[-1] == 'Z':
        date = datetime.fromisoformat(string[:-1])
    else:
        date = datetime.fromisoformat(string)

    if form == 'long':
        return date.strftime("%d.%m.%Y %H:%M:%S")
    elif form == 'short':
        return date.strftime("%d.%m.%Y")


def niceSize(size, unit='Byte'):
    """
    převádí jednotky velikosti. Metoda best_prefix sama vybere nejlepší
    jednotku a zaoukrohlí na dvě desetinna místa. Možné dát velikost v bitech
    nebo bytech (defaultně) a 'NA' je defaultní hodnota pro nevyplněné pole
    """
    if size == 'NA':
        return 'NA'

    if unit == 'Byte':
        size = Byte(int(size))
    if unit == "Bit":
        size = Bit(int(size))

    return "%s" % (size.best_prefix(system=SI).format("{value:.2f} {unit}"))
