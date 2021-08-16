from apps.secondary.models import SecondaryBase


def secondary_filter(secondary: SecondaryBase, outfit, type_station, point) -> SecondaryBase:

    if outfit is not None and outfit != '':
        secondary = secondary.filter(outfit=outfit)
    if type_station is not None and type_station != '':
        secondary = secondary.filter(type_station=type_station)
    if point is not None and point != '':
        secondary = secondary.filter(point = point)
    return secondary

def secondary_distinct(secondary: SecondaryBase, *args):
    return secondary.order_by(*args).distinct(*args)