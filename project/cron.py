import datetime
from apps.dispatching.models import Event
from apps.logging.models import ActivityLogModel


def clear_db():
    now_date = datetime.now()
    Event.objects.filter(created_at__lte__date=datetime.datetime.now() - datetime.timedelta(days=3*365)).delete()

def clear_activity_logs():
    ActivityLogModel.objects.filter(action_time__date__lte=datetime.datetime.now() - datetime.timedelta(days=365)).delete()