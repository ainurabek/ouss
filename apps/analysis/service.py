from datetime import datetime

from apps.opu.objects.models import Object
from datetime import datetime


def get_period(obj, date_to):
    if obj.date_to != None and obj.date_from != None:
        date = (obj.date_to) - (obj.date_from)
        period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100
        return period_of_time

    if obj.date_to == None:
        if date_to is not None:
            date = date_to - obj.date_from
            period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100
            return period_of_time
        date = datetime.now()
        newdate = date.replace(hour=23, minute=59, second=59)

        date = newdate - obj.date_from
        period_of_time = (((date.total_seconds() / 60) * 100) / 60) / 100
        return period_of_time












