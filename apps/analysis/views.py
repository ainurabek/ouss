import copy
from pprint import pprint

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from knox.auth import TokenAuthentication
import datetime

from apps.analysis.models import FormAnalysis, Punkt7, TotalData, Punkt5
from apps.analysis.serializers import DispEvent1ListSerializer, FormAnalysisSerializer, FormAnalysisDetailSerializer, \
    Punkt5ListSerializer, Punkt5UpdateSerializer, Punkt7UpdateSerializer, FormAnalysisUpdateSerializer, \
    Punkt7ListSerializer, FormAnalysisCreateSerializer
from django.http import JsonResponse

from apps.analysis.service import get_period, get_type_line, get_calls_list, get_amount_of_channels, \
    update_punkt5, delete_punkt5, update_punkt7, delete_punkt7, create_form_analysis_and_punkt5_punkt7, event_distinct, \
    event_filter_date_from_date_to_and_outfit, get_count_event, get_sum_period_of_time_event, determine_the_winner, \
    set_response_for_winners, get_winners

from apps.dispatching.models import Event, HistoricalEvent, Index
from apps.dispatching.services import get_event_name, get_event
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from apps.opu.services import ListWithPKMixin

from apps.analysis.service import get_diff
from rest_framework.decorators import permission_classes
from apps.accounts.permissions import SuperUser, IsAKOnly, IngenerUser




# def get_report(request):
#     date_from = request.GET.get("date_from")
#     date_to = request.GET.get("date_to")
#     responsible_outfit = request.GET.getlist("responsible_outfit")
#
#     all_event = Event.objects.filter(index1__index='1', callsorevent=False)
#     all_event = event_filter_date_from_date_to_and_outfit(all_event, date_from, date_to, responsible_outfit)
#     all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")
#     outfits = event_distinct(all_event, "ips_id", "object_id", "circuit_id")
#
#     data = []
#
#     for outfit in outfits:
#         total_outfit = {"name1": 0, "name2": 0, "name3": 0, "name4": 0, 'name5':0, 'name6':0,
#                         'name7':0, 'name8':0, 'name9':0, 'name10':0 }
#         data.append({
#             "name": outfit.responsible_outfit.outfit,
#             "date_from": None, "comments": None,
#             "reason": None, "type_line": None, "color":'1',
#             "period_of_time": {"name1": None, "name2": None, "name3": None,
#                                "name4": None, "name5": None, "name6":None,
#                                "name7": None, "name8": None, "name9":None, 'name10': None}, "amount_of_channels": None
#         })
#         for event in all_event_name.filter(responsible_outfit=outfit.responsible_outfit):
#             data.append({
#                 "name": get_event_name(event),
#                 "date_from": None, "comments": None,
#                 "reason": None, "type_line": None,
#                 "period_of_time": {"name1": None, "name2": None, "name3": None,
#                                    "name4": None, "name5":None, "name6":None,
#                                    "name7": None, "name8": None, "name9": None, 'name10': None
#                                    },
#                 "amount_of_channels": None
#             })
#             total_period_of_time = {"name1": 0, "name2": 0, "name3": 0, "name4": 0,
#                                     'name5':0, 'name6':0, 'name7':0, 'name8':0, 'name9':0, 'name10':0}
#
#
#             for call in get_calls_list(all_event, event):
#                 period = get_period(call, date_to)
#
#                 type_line = get_type_line(call)
#                 amount_of_channels = get_amount_of_channels(call)
#                 period_reason = {"name1": None, "name2": None, "name3": None, "name4": None,
#                                  "name5":None, "name6":None, "name7":None, "name8":None, 'name9':None,
#                                  'name10':None}
#                 if call.reason.name == 'Откл. ЭЭ' and type_line == 'КЛС':
#                     total_period_of_time["name1"] += period
#                     period_reason["name1"] = period
#                 elif call.reason.name == 'Откл. ЭЭ' and type_line == 'ЦРРЛ':
#                     total_period_of_time["name2"] += period
#                     period_reason["name2"] = period
#                 elif call.reason.name == 'ПВ аппаратура' and type_line=='КЛС':
#                     total_period_of_time["name3"] += period
#                     period_reason["name3"] = period
#                 elif call.reason.name == 'ПВ аппаратура' and type_line=='ЦРРЛ':
#                     total_period_of_time["name4"] += period
#                     period_reason["name4"] = period
#                 elif call.reason.name == 'Линейные ПВ' and type_line == 'КЛС':
#                     total_period_of_time["name5"] += period
#                     period_reason["name5"] = period
#                 elif call.reason.name == 'Линейные ПВ' and type_line == 'ЦРРЛ':
#                     total_period_of_time["name6"] += period
#                     period_reason["name6"] = period
#                 elif call.reason.name == 'Хищения на ЛС' and type_line =='КЛС':
#                     total_period_of_time["name7"] += period
#                     period_reason["name7"] = period
#                 elif call.reason.name == 'Хищения на ЛС' and type_line =='ЦРРЛ':
#                     total_period_of_time["name8"] += period
#                     period_reason["name8"] = period
#                 elif call.reason.name == 'ПВ за счет стихии' and type_line =='КЛС':
#                     total_period_of_time["name9"] += period
#                     period_reason["name9"] = period
#                 elif call.reason.name == 'ПВ за счет стихии' and type_line =='ЦРРЛ':
#                     total_period_of_time["name10"] += period
#                     period_reason["name10"] = period
#
#                 data.append({
#                     "name": None, "date_from": call.date_from,
#                     "date_to": call.date_to, "comments": call.comments1,
#                     "reason": call.reason.id, "type_line": type_line,
#                     "period_of_time": period_reason, "amount_of_channels": amount_of_channels
#                 })
#
#
#             total = dict(total_period_of_time)
#
#             for i in total:
#                 total[i] = round(total[i] * int(get_amount_of_channels(event)), 2)
#
#                 total_outfit[i] += total[i]
#
#             data.append({
#                 "name": "всего", "date_from": "час", "comments": None,
#                 "reason": None, "type_line": get_type_line(event),
#                 "period_of_time": total_period_of_time,   "color":'2'
#             })
#
#             data.append({
#                 "name": "всего", "date_from": "кнл/час", "comments": None,
#                 "reason": None, "type_line": get_type_line(event),
#                 "period_of_time": total,   "color":'3'
#             })
#
#         data.append({
#             "name": "Общий итог", "date_from": None, "comments": None,
#             "reason": None, "type_line": None,
#             "period_of_time": total_outfit,  "color":'4'
#         })
#
#     return JsonResponse(data, safe=False)



@permission_classes([IsAuthenticated, SuperUser|IsAKOnly])
def get_report(request):
    """Отчет по 1. Форма анализа"""
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    responsible_outfit = request.GET.getlist("responsible_outfit[]")

    all_event = Event.objects.filter(index1__index='1', callsorevent=False, reason__name__in=['Откл. ЭЭ', 'ПВ аппаратура',
                                                                                              'Линейные ПВ', 'Хищения на ЛС', 'ПВ за счет стихии'])
    all_event = event_filter_date_from_date_to_and_outfit(all_event, date_from, date_to, responsible_outfit)
    all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")
    outfits = event_distinct(all_event, "ips_id", "object_id", "circuit_id")

    data = []

    list_reason_typ_line = {
        "Откл. ЭЭКЛС": None, "Откл. ЭЭЦРРЛ": None, "ПВ аппаратураКЛС": None,
        "ПВ аппаратураЦРРЛ": None, "Линейные ПВКЛС": None, "Линейные ПВЦРРЛ": None,
        "Хищения на ЛСКЛС": None, "Хищения на ЛСЦРРЛ": None, "ПВ за счет стихииКЛС": None, 'ПВ за счет стихииЦРРЛ': None
        }

    example = {"name": None, "date_from": None, "comments": None, "period_of_time": list_reason_typ_line.copy(),
               'color': None, "amount_of_channels": {"КЛС": None, "ЦРРЛ": None}
    }

    for outfit in outfits:
        total_outfit = copy.deepcopy(example)
        total_outfit['period_of_time'] = dict.fromkeys(list_reason_typ_line, 0)
        out_data = copy.deepcopy(example)
        out_data['name'] = outfit.responsible_outfit.outfit
        out_data['color'] = "1"
        data.append(out_data)

        for event in all_event_name.filter(responsible_outfit=outfit.responsible_outfit):
            event_data = copy.deepcopy(example)
            event_data['name'] = get_event_name(event)
            data.append(event_data)
            example['period_of_time'] = dict.fromkeys(list_reason_typ_line, 0)
            total_period_of_time = copy.deepcopy(example)

            for call in get_calls_list(all_event, event):
                period = get_period(call, date_to)

                if call.ips is None:
                    type_line = get_type_line(call)
                    amount_of_channels = get_amount_of_channels(call)

                    call_data = copy.deepcopy(example)
                    call_data['period_of_time'][call.reason.name+type_line] = period

                    call_data['amount_of_channels'][type_line] = amount_of_channels

                    total_period_of_time['period_of_time'][call.reason.name+type_line] += period

                    data.append(call_data)
                else:
                    call_data = copy.deepcopy(example)
                    kls = call.ips.total_point_channels_KLS
                    rrl = call.ips.total_point_channels_RRL

                    if kls != 0:
                        call_data['period_of_time'][call.reason.name + 'КЛС'] = period
                        total_period_of_time['period_of_time'][call.reason.name + 'КЛС'] += period

                    if rrl != 0:
                        call_data['period_of_time'][call.reason.name + 'ЦРРЛ'] = period
                        total_period_of_time['period_of_time'][call.reason.name + 'ЦРРЛ'] += period

            total = dict(total_period_of_time)
            if event.ips is None:
                for i in total['period_of_time']:
                    total['period_of_time'][i] = round(total['period_of_time'][i] * int(get_amount_of_channels(event)), 2)
                    total_outfit['period_of_time'][i] += total['period_of_time'][i]
            else:
                k = event.ips.total_point_channels_KLS
                r = event.ips.total_point_channels_RRL

                for i in total['period_of_time']:
                    if k != 0:
                        total['period_of_time'][i] = round(total['period_of_time'][i] * k, 2)
                        total_outfit['period_of_time'][i] += total['period_of_time'][i]
                    if r != 0:
                        total['period_of_time'][i] = round(total['period_of_time'][i] * r, 2)
                        total_outfit['period_of_time'][i] += total['period_of_time'][i]

            total_period_of_time['name'] = 'всего'
            total_period_of_time['date_from'] = 'час'
            total_period_of_time['color'] = '2'
            data.append(total_period_of_time)
            total['name'] = 'всего'
            total['date_from'] = 'кнл/час'
            total['color'] = '3'
            data.append(total)

        total_outfit['name'] = 'Общий итог'
        total_outfit['color'] = '4'
        data.append(total_outfit)
    return JsonResponse(data, safe=False)

@permission_classes([IsAuthenticated, SuperUser|IsAKOnly])
def get_report_analysis(request):
    """Отчет дисп.службы по разным индексам"""
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    index = request.GET.get("index")
    responsible_outfit = request.GET.getlist('responsible_outfit')

    all_event_completed = Event.objects.filter(callsorevent=True, index1__index='4')

    all_event_completed = event_filter_date_from_date_to_and_outfit(all_event_completed, date_from, date_to, responsible_outfit)

    all_event_uncompleted = Event.objects.filter(callsorevent=True).exclude(index1__index='4')
    all_event_uncompleted = event_filter_date_from_date_to_and_outfit(all_event_uncompleted, date_from, date_to, responsible_outfit)
    all_event = all_event_completed | all_event_uncompleted
    all_calls = Event.objects.filter(callsorevent=False)
    if index is not None:
        all_calls = all_calls.filter(index1_id=index)

    outfits = (all_event_completed | all_event_uncompleted).order_by("responsible_outfit").distinct(
        "responsible_outfit")

    data = []

    example = {"outfit": None, 'id': None, "name": None, "reason": None,
               "date_from": None,  "date_to": None, 'region': None,
               "index1": None, "comments1": None}

    for out in outfits:
        out_data = example.copy()
        out_data['outfit'] = out.responsible_outfit.outfit
        data.append(out_data)
        for event in all_event.filter(responsible_outfit=out.responsible_outfit):
            event_data = example.copy()
            event_data['id'] = event.id
            event_data['name'] = get_event_name(event)
            data.append(event_data)
            calls_count = 0
            for call in all_calls.filter(id_parent=event).exclude(index1__index='4'):
                call_data = example.copy()
                call_data['id'] = call.id
                call_data['name'] = get_event_name(call)
                call_data['reason'] = call.reason.name
                call_data['date_from'] = call.date_from
                call_data['date_to'] = call.date_to
                call_data['region'] = call.point1.point + " - " + call.point2.point if call.point1 is not None else ""
                call_data['comments1'] = call.comments1
                call_data['index1'] = call.index1.index
                data.append(call_data)
                calls_count += 1
            if calls_count == 0:
                data.pop()

    return JsonResponse(data, safe=False)


class DispEventHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)

    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        histories = event.history.all()
        data = []
        for h in histories:
            a = {}
            a['history_id'] = h.history_id
            a['updated_date'] = h.history_date
            a['updated_by'] = h.history_user.username
            a['change_method'] = h.get_history_type_display()
            a['changes'] = get_diff(history=h)
            if a['changes'] == "" and h.history_type == '~':
                continue
            data.append(a)
        return Response(data, status=status.HTTP_200_OK)


class FormAnalysisAPIViewSet(viewsets.ModelViewSet):
    """Отчет по коэф, пункт 5, пункт 7 - Отчет АК"""
    authentication_classes = (TokenAuthentication,)
    queryset = FormAnalysis.objects.filter(main=True).order_by('-id')
    lookup_field = 'pk'

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, SuperUser|IsAKOnly]
        else:
            permission_classes = [IsAuthenticated, SuperUser|IsAKOnly, IngenerUser]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FormAnalysisDetailSerializer
        else:
            return FormAnalysisSerializer

    def perform_create(self, serializer):

        """Создание парентев для обектов"""
        analysis_form = serializer.save(user=self.request.user.profile, main=True)
        analysis_form.id_parent = analysis_form
        analysis_form.save()
        punkt5 = Punkt5.objects.create(user=self.request.user.profile, form_analysis=analysis_form)
        punkt7 = Punkt7.objects.create(user=self.request.user.profile, form_analysis=analysis_form)
        TotalData.objects.create(punkt7=punkt7)
        TotalData.objects.create(punkt5=punkt5)

    def retrieve(self, request, *args, **kwargs):
        """ Список ср.КФТ отчет """
        form_list = FormAnalysis.objects.filter(id_parent=self.get_object().pk).order_by('-id')
        serializer = self.get_serializer(form_list, many=True)
        return Response(serializer.data)


class FormAnalysisUpdateAPIView(generics.UpdateAPIView):
    """Редактирование п.5"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly, IngenerUser)
    lookup_field = "pk"
    queryset = FormAnalysis.objects.all()
    serializer_class = FormAnalysisUpdateSerializer


class FormAnalysisCreateAPIView(APIView):
    """ Создание ср.КФТ отчета """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly, IngenerUser)

    def post(self, request, pk):
        outfit = request.data['outfit']

        if FormAnalysis.objects.filter(id_parent__id=pk, outfit__id=outfit).exclude(id=pk).exists():
            content = {'По такому предприятию уже существует Средний Коэффициент'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        else:
            date_from = request.data["date_from"]
            date_to = request.data["date_to"]
            outfit = request.data["outfit"]
            punkt7_AK = request.data["form_analysis"]
            serializer = FormAnalysisCreateSerializer(data=request.data)
            if serializer.is_valid():
                parent = FormAnalysis.objects.get(pk=pk)
                create_form_analysis_and_punkt5_punkt7(date_from, date_to, outfit, punkt7_AK, parent, request.user.profile)
                data = {"response": "Успешно создан"}
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Punkt5ListAPIView(APIView, ListWithPKMixin):
    """Список п.5"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)
    model = Punkt5
    serializer = Punkt5ListSerializer
    field_for_filter = "form_analysis__id_parent"


class Punkt7ListAPIView(APIView, ListWithPKMixin):
    """Список п.5"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)
    model = Punkt7
    serializer = Punkt7ListSerializer
    field_for_filter = "form_analysis__id_parent"


class Punkt5UpdateAPIView(generics.UpdateAPIView):
    """Редактирование п.5"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly, IngenerUser)
    lookup_field = "pk"
    queryset = Punkt5.objects.all()
    serializer_class = Punkt5UpdateSerializer

    def perform_update(self, serializer):
        punkt5 = serializer.save()
        update_punkt5(punkt5)


class Punkt5DeleteAPIVIew(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly, IngenerUser)
    queryset = Punkt5.objects.all()
    lookup_field = "pk"

    def perform_destroy(self, instance):
        delete_punkt5(instance)


class Punkt7UpdateAPIView(generics.UpdateAPIView):
    """Редактирование п.7"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly, IngenerUser)
    lookup_field = "pk"
    queryset = Punkt7.objects.all()
    serializer_class = Punkt7UpdateSerializer

    def perform_update(self, serializer):
        puknkt5 = serializer.save()
        update_punkt7(puknkt5)


class Punkt7DeleteAPIView(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly, IngenerUser)
    queryset = Punkt7.objects.all()
    lookup_field = "pk"

    def perform_destroy(self, instance):
        delete_punkt7(instance)


class ReportOaAndOdApiView(APIView):
    """Отчет по Од, Оа, Отв"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)

    def get(self, request):
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        responsible_outfit = request.GET.getlist("responsible_outfit")
        index = request.GET.get("index")
        od = Index.objects.get(index="0д")
        oa = Index.objects.get(index="0а")
        otv = Index.objects.get(index="0тв")

        if index is None or index == '':
            all_event = Event.objects.filter(index1__in=[od, oa, otv])
        elif od.id == index or oa.id == index or otv.id == index:
            all_event = Event.objects.filter(index1__in=[index],
                                         callsorevent=False)
        else:
            message = {'message': "Можно фильтровать только по индекса Од, Оа, Отв"}
            return Response(message, status.HTTP_403_FORBIDDEN)

        all_event = event_filter_date_from_date_to_and_outfit(all_event, date_from, date_to, responsible_outfit)
        outfits = event_distinct(all_event, "responsible_outfit")
        all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")
        data = []

        winners_otv = {
            "first": {"value": 0, "index": None},
            "second": {"value": 0, "index": None},
            "third": {"value": 0, "index": None}
        }

        winners_oa = {
            "first": {"value": 0, "index": None},
            "second": {"value": 0, "index": None},
            "third": {"value": 0, "index": None}
        }

        winners_od = {
            "first": {"value": 0, "index": None},
            "second": {"value": 0, "index": None},
            "third": {"value": 0, "index": None}
        }
        rep = {
            "outfit": None,
            "name": None,
            "oa": {"sum": 0, "count": 0},
            "od": {"sum": 0, "count": 0},
            "otv": {"sum": 0, "count": 0},
            "total_sum": {"sum": 0, "count": 0}

        }

        for out in outfits:
            outfit = out.responsible_outfit
            data.append({"outfit": outfit.outfit, "name": None, "total_sum": {"sum": None, "count": None}, "oa": {"sum": None, "count": None}, "od": {"sum": None, "count": None},
                    "otv": {"sum": None, "count": None}})
            outfit_data = {"outfit": outfit.outfit, "name": None, "total_sum": {"sum": 0, "count": 0}, "oa": {"sum": 0, "count": 0}, "od": {"sum": 0, "count": 0},
                    "otv": {"sum": 0, "count": 0}}
            for event in all_event_name.filter(responsible_outfit=outfit):
                count_od = get_count_event(all_event, get_event(event), od, outfit)
                count_oa = get_count_event(all_event, get_event(event), oa, outfit)

                count_otv = get_count_event(all_event, get_event(event), otv, outfit)
                sum_oa = get_sum_period_of_time_event(all_event, get_event(event), oa, outfit)
                sum_otv = get_sum_period_of_time_event(all_event, get_event(event), otv, outfit)
                sum_od = get_sum_period_of_time_event(all_event, get_event(event), od, outfit)

                winner_index = len(data)
                winners_otv = determine_the_winner(winners_otv, sum_otv, winner_index)
                winners_oa = determine_the_winner(winners_oa, sum_oa, winner_index)
                winners_od = determine_the_winner(winners_od, sum_od, winner_index)

                data.append({"name": get_event_name(event), "outfit": None,
                                       "total_sum": {"sum": sum_oa+sum_od+sum_otv, "count": count_oa + count_od + count_otv, "color": None},
                                       "oa": {"sum": sum_oa, "count": count_oa, "color": None},
                                       "od": {"sum": sum_od, "count": count_od, "color": None},
                                       "otv": {"sum": sum_otv, "count": count_otv, "color": None}})
                outfit_data["oa"]["count"] += count_oa
                outfit_data["od"]["count"] += count_od
                outfit_data["otv"]["count"] += count_otv
                outfit_data["oa"]["sum"] += sum_oa
                outfit_data["od"]["sum"] += sum_od
                outfit_data["otv"]["sum"] += sum_otv
                outfit_data['total_sum']['sum'] = round(outfit_data['total_sum']['sum']+ sum_oa+sum_od+sum_otv, 2)
                outfit_data['total_sum']['count'] += count_oa + count_od + count_otv

            rep["oa"]["count"] +=  outfit_data["oa"]["count"]
            rep["od"]["count"] +=  outfit_data["od"]["count"]
            rep["otv"]["count"] +=  outfit_data["otv"]["count"]
            rep["oa"]["sum"] += outfit_data["oa"]["sum"]
            rep["od"]["sum"] += outfit_data["od"]["sum"]
            rep["otv"]["sum"] += outfit_data["otv"]["sum"]
            rep['total_sum']['sum'] = round(rep['total_sum']['sum'] + outfit_data["oa"]["sum"] + outfit_data["od"]["sum"]+outfit_data["otv"]["sum"], 2)
            rep['total_sum']['count'] += outfit_data["oa"]["count"]+outfit_data["od"]["count"]+outfit_data["otv"]["count"]
            winners_oa = set_response_for_winners(winners_oa, "oa", data)
            winners_od = set_response_for_winners(winners_od, "od", data)
            winners_otv = set_response_for_winners(winners_otv, "otv", data)
            data.append(outfit_data)
        data.append(rep)
        return JsonResponse(data, safe=False)


class WinnerReportAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)

    def get(self, request):
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        responsible_outfit = request.GET.getlist("responsible_outfit")
        index_id = request.GET.get('index')
        if index_id is None:
            od = Index.objects.get(index="0д")
            oa = Index.objects.get(index="0а")
            otv = Index.objects.get(index="0тв")
            list_index = [oa, otv, od]
        else:
            list_index = [Index.objects.get(pk=index_id)]

        all_event = Event.objects.filter(index1__in=list_index, callsorevent=False)
        all_event = event_filter_date_from_date_to_and_outfit(all_event, date_from, date_to, responsible_outfit)
        outfits = event_distinct(all_event, "responsible_outfit")
        all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")
        winners = {i.index: [{"name": None, "sum": 0, "count": 0} for _ in range(3)] for i in list_index}
        data = []

        for out in outfits:
            outfit = out.responsible_outfit
            for index in list_index:
                for event in all_event_name.filter(responsible_outfit=outfit, index1=index):
                    sum = get_sum_period_of_time_event(all_event, get_event(event), index, outfit)
                    count = get_count_event(all_event, get_event(event), index, outfit)
                    event_name = get_event_name(event)
                    get_winners(winners[index.index], event_name, sum, count)

                data.append({"outfit": outfit.outfit, "index": index.index, "winners": winners[index.index]})

        return JsonResponse(data, safe=False)