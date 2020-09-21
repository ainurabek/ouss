from django.http import JsonResponse

from apps.analysis.service import get_period, get_type_line, get_calls_list, get_amount_of_channels
from apps.dispatching.models import Event
from apps.dispatching.services import get_event_name


def get_report(request):
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    responsible_outfit = request.GET.get("responsible_outfit")
    all_event = Event.objects.filter(index1_id=6, callsorevent=False)

    if responsible_outfit != "":
        all_event = all_event.filter(responsible_outfit_id=responsible_outfit)

    if date_from != "" and date_to == "":
        all_event = all_event.filter(created_at=date_from)
    elif date_from == "" and date_to != "":
        all_event = all_event.filter(created_at=date_to)
    elif date_from != "" and date_to != "":
        all_event = all_event.filter(created_at__gte=date_from, created_at__lte=date_to)

    all_event_name = all_event.order_by("ips_id", "object_id", "circuit_id").distinct("ips_id", "object_id", "circuit_id")

    outfits = all_event.order_by("responsible_outfit").distinct("responsible_outfit")

    data = []
    for outfit in outfits:
        total_outfit = {"1": 0, "2": 0, "3": 0, "4": 0}
        data.append({
            "name": outfit.responsible_outfit.outfit,
            "date_from": None, "comments": None,
            "reason": None, "type_line": None,
            "period_of_time": None, "amount_of_channels": None
        })
        for event in all_event_name.filter(responsible_outfit=outfit.responsible_outfit):
            data.append({
                "name": get_event_name(event),
                "date_from": None, "comments": None,
                "reason": None, "type_line": None,
                "period_of_time": None, "amount_of_channels": None
            })
            total_period_of_time = {"1": 0, "2": 0, "3": 0, "4": 0}

            for call in get_calls_list(all_event, event):
                period = get_period(call, date_to)
                type_line = get_type_line(call)
                amount_of_channels = get_amount_of_channels(call)
                if call.reason.id == 1:
                    total_period_of_time["1"] += period
                elif call.reason.id == 2:
                    total_period_of_time["2"] += period

                data.append({
                    "name": None, "date_from": call.date_from,
                    "date_to": call.date_to, "comments": call.comments1,
                    "reason": call.reason.id, "type_line": type_line,
                    "period_of_time": period, "amount_of_channels": amount_of_channels
                })

            total = dict(total_period_of_time)
            for i in total:
                total[i] = total[i] * int(get_amount_of_channels(event))
                total_outfit[i] += total[i]
            data.append({
                "name": "всего", "date_from": "час", "comments": None,
                "reason": None, "type_line": get_type_line(event),
                "total_hours": total_period_of_time
            })

            data.append({
                "name": "всего", "date_from": "час", "comments": None,
                "reason": None, "type_line": get_type_line(event),
                "total_channel_in_hours": total
            })

        data.append({
            "name": "всего", "date_from": "час", "comments": None,
            "reason": None, "type_line": get_type_line(event),
            "total_outfit": total_outfit
        })

    return JsonResponse(data, safe=False)