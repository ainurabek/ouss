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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from apps.opu.services import ListWithPKMixin

from apps.analysis.service import get_diff


def get_report(request):
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    responsible_outfit = request.GET.get("responsible_outfit")

    all_event = Event.objects.filter(index1__index='1', callsorevent=False)
    all_event = event_filter_date_from_date_to_and_outfit(all_event, date_from, date_to, responsible_outfit)
    all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")
    outfits = event_distinct(all_event, "ips_id", "object_id", "circuit_id")

    data = []

    for outfit in outfits:
        total_outfit = {"name1": 0, "name2": 0, "name3": 0, "name4": 0, 'name5':0, 'name6':0,
                        'name7':0, 'name8':0, 'name9':0, 'name10':0 }
        data.append({
            "name": outfit.responsible_outfit.outfit,
            "date_from": None, "comments": None,
            "reason": None, "type_line": None, "color":'1',
            "period_of_time": {"name1": None, "name2": None, "name3": None,
                               "name4": None, "name5":None, "name6":None,
                               "name7": None, "name8":None, "name9":None, 'name10':None}, "amount_of_channels": None
        })
        for event in all_event_name.filter(responsible_outfit=outfit.responsible_outfit):
            data.append({
                "name": get_event_name(event),
                "date_from": None, "comments": None,
                "reason": None, "type_line": None,
                "period_of_time": {"name1": None, "name2": None, "name3": None,
                                   "name4": None, "name5":None, "name6":None,
                                   "name7": None, "name8": None, "name9": None, 'name10': None
                                   },
                "amount_of_channels": None
            })
            total_period_of_time = {"name1": 0, "name2": 0, "name3": 0, "name4": 0,
                                    'name5':0, 'name6':0, 'name7':0, 'name8':0, 'name9':0, 'name10':0}


            for call in get_calls_list(all_event, event):
                period = get_period(call, date_to)
                type_line = get_type_line(call)
                amount_of_channels = get_amount_of_channels(call)
                period_reason = {"name1": None, "name2": None, "name3": None, "name4": None,
                                 "name5":None, "name6":None, "name7":None, "name8":None, 'name9':None,
                                 'name10':None}
                if call.reason.name == 'Откл. ЭЭ' and type_line == 'КЛС':
                    total_period_of_time["name1"] += period
                    period_reason["name1"] = period
                elif call.reason.name == 'Откл. ЭЭ' and type_line == 'ЦРРЛ':
                    total_period_of_time["name2"] += period
                    period_reason["name2"] = period
                elif call.reason.name == 'ПВ аппаратура' and type_line=='КЛС':
                    total_period_of_time["name3"] += period
                    period_reason["name3"] = period
                elif call.reason.name == 'ПВ аппаратура' and type_line=='ЦРРЛ':
                    total_period_of_time["name4"] += period
                    period_reason["name4"] = period
                elif call.reason.name == 'Линейные ПВ' and type_line == 'КЛС':
                    total_period_of_time["name5"] += period
                    period_reason["name5"] = period
                elif call.reason.name == 'Линейные ПВ' and type_line == 'ЦРРЛ':
                    total_period_of_time["name6"] += period
                    period_reason["name6"] = period
                elif call.reason.name == 'Хищения на ЛС' and type_line =='КЛС':
                    total_period_of_time["name7"] += period
                    period_reason["name7"] = period
                elif call.reason.name == 'Хищения на ЛС' and type_line =='ЦРРЛ':
                    total_period_of_time["name8"] += period
                    period_reason["name8"] = period
                elif call.reason.name == 'ПВ за счет стихии' and type_line =='КЛС':
                    total_period_of_time["name9"] += period
                    period_reason["name9"] = period
                elif call.reason.name == 'ПВ за счет стихии' and type_line =='ЦРРЛ':
                    total_period_of_time["name10"] += period
                    period_reason["name10"] = period

                data.append({
                    "name": None, "date_from": call.date_from,
                    "date_to": call.date_to, "comments": call.comments1,
                    "reason": call.reason.id, "type_line": type_line,
                    "period_of_time": period_reason, "amount_of_channels": amount_of_channels
                })

            total = dict(total_period_of_time)
            for i in total:
                total[i] = total[i] * int(get_amount_of_channels(event))
                total_outfit[i] += total[i]
            data.append({
                "name": "всего", "date_from": "час", "comments": None,
                "reason": None, "type_line": get_type_line(event),
                "period_of_time": total_period_of_time, "color":'2'
            })

            data.append({
                "name": "всего", "date_from": "кнл/час", "comments": None,
                "reason": None, "type_line": get_type_line(event),
                "period_of_time": total, "color":'3'
            })

        data.append({
            "name": "Общий итог", "date_from": None, "comments": None,
            "reason": None, "type_line": None,
            "period_of_time": total_outfit, "color":'4'
        })

    return JsonResponse(data, safe=False)


class DispEvent1ListAPIView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Event.objects.filter(callsorevent=False, index1__index="1")
    lookup_field = 'pk'
    serializer_class = DispEvent1ListSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('object', 'ips', 'circuit', 'responsible_outfit',)

    def get_queryset(self):
        today = datetime.date.today()
        queryset = self.queryset.filter(created_at=today)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        if date_to == "" and date_from != '':
            queryset = self.queryset.filter(created_at=date_from)
        elif date_to != '' and date_from == '':
            queryset = self.queryset.filter(created_at=date_to)
        elif date_to != '' and date_from != '':
            queryset = self.queryset.filter(created_at__gte=date_from, created_at__lte=date_to)

        return queryset


class DispEventHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
            if a['changes'] == "" and h.history_type =='~':
                continue
            data.append(a)
        return Response(data, status=status.HTTP_200_OK)


class FormAnalysisAPIViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = FormAnalysis.objects.filter(main=True).order_by('-id')
    lookup_field = 'pk'

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
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"
    queryset = FormAnalysis.objects.all()
    serializer_class = FormAnalysisUpdateSerializer


class FormAnalysisCreateAPIView(APIView):
    """ Создание ср.КФТ отчета """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        if FormAnalysis.objects.filter(id_parent_id=pk, outfit_id=request.data["outfit"]).exists():
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
    permission_classes = (IsAuthenticated,)
    model = Punkt5
    serializer = Punkt5ListSerializer
    field_for_filter = "form_analysis__id_parent"


class Punkt7ListAPIView(APIView, ListWithPKMixin):
    """Список п.5"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Punkt7
    serializer = Punkt7ListSerializer
    field_for_filter = "form_analysis__id_parent"


class Punkt5UpdateAPIView(generics.UpdateAPIView):
    """Редактирование п.5"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"
    queryset = Punkt5.objects.all()
    serializer_class = Punkt5UpdateSerializer

    def perform_update(self, serializer):
        punkt5 = serializer.save()
        update_punkt5(punkt5)


class Punkt5DeleteAPIVIew(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Punkt5.objects.all()
    lookup_field = "pk"

    def perform_destroy(self, instance):
        delete_punkt5(instance)


class Punkt7UpdateAPIView(generics.UpdateAPIView):
    """Редактирование п.7"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"
    queryset = Punkt7.objects.all()
    serializer_class = Punkt7UpdateSerializer

    def perform_update(self, serializer):
        puknkt5 = serializer.save()
        update_punkt7(puknkt5)


class Punkt7DeleteAPIView(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Punkt7.objects.all()
    lookup_field = "pk"

    def perform_destroy(self, instance):
        delete_punkt7(instance)


class ReportOaAndOdApiView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        outfit = request.GET.get("outfit")
        od = Index.objects.get(index="0д")
        oa = Index.objects.get(index="0а")
        otv = Index.objects.get(index="Отв")

        all_event = Event.objects.filter(index1__in=[od, oa, otv],
                                         callsorevent=False)
        all_event = event_filter_date_from_date_to_and_outfit(all_event, date_from, date_to, outfit)
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
            "events": [],
            "oa": {"sum": 0, "count": 0},
            "od": {"sum": 0, "count": 0},
            "otv": {"sum": 0, "count": 0}

        }

        for out in outfits:
            outfit = out.responsible_outfit
            base = {"outfit": outfit.outfit, "events": [], "oa": {"sum": 0, "count": 0}, "od": {"sum": 0, "count": 0},
                    "otv": {"sum": 0, "count": 0}}

            for event in all_event_name.filter(responsible_outfit=outfit):
                count_od = get_count_event(all_event, get_event(event), od, outfit)
                count_oa = get_count_event(all_event, get_event(event), oa, outfit)
                count_otv = get_count_event(all_event, get_event(event), otv, outfit)
                sum_oa = get_sum_period_of_time_event(all_event, get_event(event), oa, outfit)
                sum_otv = get_sum_period_of_time_event(all_event, get_event(event), otv, outfit)
                sum_od = get_sum_period_of_time_event(all_event, get_event(event), od, outfit)

                winner_index = len(base["events"])
                winners_otv = determine_the_winner(winners_otv, sum_otv, winner_index)
                winners_oa = determine_the_winner(winners_oa, sum_oa, winner_index)
                winners_od = determine_the_winner(winners_od, sum_od, winner_index)

                base["events"].append({"name": get_event_name(event),
                                       "oa": {"sum": sum_oa, "count": count_oa, "color": None},
                                       "od": {"sum": sum_od, "count": count_od, "color": None},
                                       "otv": {"sum": sum_otv, "count": count_otv, "color": None}})
                base["oa"]["count"] += count_oa
                base["od"]["count"] += count_od
                base["otv"]["count"] += count_otv
                base["oa"]["sum"] += sum_oa
                base["od"]["sum"] += sum_od
                base["otv"]["sum"] += sum_otv

            rep["oa"]["count"] +=  base["oa"]["count"]
            rep["od"]["count"] +=  base["od"]["count"]
            rep["otv"]["count"] +=  base["otv"]["count"]
            rep["oa"]["sum"] += base["oa"]["sum"]
            rep["od"]["sum"] += base["od"]["sum"]
            rep["otv"]["sum"] += base["otv"]["sum"]

            winners_oa = set_response_for_winners(winners_oa, "oa", base["events"])
            winners_od = set_response_for_winners(winners_od, "od", base["events"])
            winners_otv = set_response_for_winners(winners_otv, "otv", base["events"])
            data.append(base)
        data.append(rep)
        return JsonResponse(data, safe=False)


class WinnerReportAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        outfit = request.GET.get("outfit")
        od = Index.objects.get(index="0д")
        oa = Index.objects.get(index="0а")
        otv = Index.objects.get(index="Отв")

        all_event = Event.objects.filter(index1__in=[od, oa, otv], callsorevent=False)
        all_event = event_filter_date_from_date_to_and_outfit(all_event, date_from, date_to, outfit)
        outfits = event_distinct(all_event, "responsible_outfit")
        all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")
        data = []

        winners_oa = [
            {"name": None, "sum": 0, "count": 0},
            {"name": None, "sum": 0, "count": 0},
            {"name": None, "sum": 0, "count": 0},
        ]

        winners_otv = [
            {"name": None, "sum": 0, "count": 0},
            {"name": None, "sum": 0, "count": 0},
            {"name": None, "sum": 0, "count": 0},
        ]

        winners_od = [
            {"name": None, "sum": 0, "count": 0},
            {"name": None, "sum": 0, "count": 0},
            {"name": None, "sum": 0, "count": 0},
        ]
        for out in outfits:
            outfit = out.responsible_outfit

            for event in all_event_name.filter(responsible_outfit=outfit):
                sum_oa = get_sum_period_of_time_event(all_event, get_event(event), oa, outfit)
                sum_otv = get_sum_period_of_time_event(all_event, get_event(event), otv, outfit)
                sum_od = get_sum_period_of_time_event(all_event, get_event(event), od, outfit)
                count_od = get_count_event(all_event, get_event(event), od, outfit)
                count_oa = get_count_event(all_event, get_event(event), oa, outfit)
                count_otv = get_count_event(all_event, get_event(event), otv, outfit)
                event_name = get_event_name(event)
                winners_oa = get_winners(winners_oa, event_name, sum_oa, count_oa)
                winners_od = get_winners(winners_od, event_name, sum_od, count_od)
                winners_otv = get_winners(winners_otv, event_name, sum_otv, count_otv)

            data.append({"outfit": outfit.outfit, "index": oa.name, "winners": winners_oa})
            data.append({"outfit": outfit.outfit, "index": od.name, "winners": winners_od})
            data.append({"outfit": outfit.outfit, "index": otv.name, "winners": winners_otv})

        return JsonResponse(data, safe=False)