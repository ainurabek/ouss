import datetime
from datetime import timedelta

from rest_framework.generics import ListAPIView


class ListFilterAPIView(ListAPIView):

    def get_queryset(self):
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)

        if date_to == "" and date_from == "":
            week = datetime.date.today() - timedelta(days=7)
            queryset = self.queryset.filter(created_at__gte=week)

        else:

            if date_to == "" and date_from != '':
                queryset = self.queryset.filter(created_at=date_from)
            elif date_to != '' and date_from == '':
                queryset = self.queryset.filter(created_at=date_to)
            else:
                if date_to != '' and date_from != '':
                    queryset = self.queryset.filter(created_at__gte=date_from, created_at__lte=date_to)

        return queryset


def get_minus_date(days: int):
    return datetime.date.today() - timedelta(days=days)


# def update_period_of_time(instance):
#     if instance.date_from is not None and instance.date_to is not None:
#         date = instance.date_to - instance.date_from
#         period_time=(((date.total_seconds()/60)*100)/60)/100
#         print(period_time)
#         instance.period_of_time = period_time
#         print(instance.period_of_time)
#         instance.save()
#         print(instance.period_of_time)