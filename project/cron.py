import datetime

from apps.dispatching.models import Event


def clear_db():
    now_date = datetime.now()
    Event.objects.filter(created_at__lte__date=datetime.datetime.now() - datetime.timedelta(days=3*365)).delete()
