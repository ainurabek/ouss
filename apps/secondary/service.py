from apps.secondary.models import SecondaryBase, AmbulanceNumsBase



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

def ambul_filter(ambul: AmbulanceNumsBase, outfit) -> AmbulanceNumsBase:
    if outfit is not None and outfit != '':
        ambul = ambul.filter(outfit=outfit)
    return ambul

def ambul_distinct(ambul: AmbulanceNumsBase, *args):
    return ambul.order_by(*args).distinct(*args)