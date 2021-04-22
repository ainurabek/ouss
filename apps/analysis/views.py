import copy

import matplotlib.pyplot as plt
from django.core.files.base import ContentFile
from rest_framework import viewsets, generics
from rest_framework.generics import UpdateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from apps.analysis.models import FormAnalysis, Punkt7, TotalData, Punkt5, Form61KLS
from apps.analysis.serializers import DispEvent1ListSerializer, FormAnalysisSerializer, FormAnalysisDetailSerializer, \
    Punkt5ListSerializer, Punkt5UpdateSerializer, Punkt7UpdateSerializer, FormAnalysisUpdateSerializer, \
    Punkt7ListSerializer, FormAnalysisCreateSerializer, Form61KLSCreateSerializer, Form61KLSSerializer
from django.http import JsonResponse, HttpResponse

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
from apps.analysis.service import get_date_to_ak
from apps.dispatching.services import get_date_to
from apps.analysis.models import AmountChannelsKLSRRL
from apps.analysis.serializers import AmountChannelsKLSRRLSerializer
from apps.analysis.service import get_amount
from apps.analysis.service import form61_kls_filter, form61_kls_distinct
import networkx as nx
from apps.opu.objects.models import Point
from rest_framework.viewsets import ModelViewSet
from apps.analysis.models import TypeConnection, MethodLaying, TypeCable
from apps.analysis.serializers import TypeConnectionSerializer, MethodLayingSerializer, TypeCableSerializer
import matplotlib
matplotlib.use('tkagg')


# @permission_classes([IsAuthenticated, SuperUser|IsAKOnly])
# def get_report(request):
#     """ Форма анализа"""
#     date_from = request.GET.get("date_from")
#     date_to = request.GET.get("date_to")
#     responsible_outfit = request.GET.getlist("responsible_outfit")
#
#     all_event = Event.objects.filter(index1__index='1', callsorevent=False, reason__name__in=['Откл. ЭЭ', 'ПВ аппаратуры',
#                                                                                               'Линейные ПВ', 'Хищения на ЛС', 'ПВ за счет стихии']).exclude(name__isnull=False)
#
#     all_event = event_filter_date_from_date_to_and_outfit(all_event, date_from, date_to, responsible_outfit)
#
#     all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")
#     outfits = event_distinct(all_event, "responsible_outfit")
#
#     data = []
#
#     list_reason_typ_line = {
#         "Откл. ЭЭКЛС": None, "Откл. ЭЭЦРРЛ": None, "ПВ аппаратурыКЛС": None,
#         "ПВ аппаратурыЦРРЛ": None, "Линейные ПВКЛС": None, "Линейные ПВЦРРЛ": None,
#         "Хищения на ЛСКЛС": None, "Хищения на ЛСЦРРЛ": None, "ПВ за счет стихииКЛС": None, 'ПВ за счет стихииЦРРЛ': None
#         }
#
#     example = {"name": None, "date_from": None, "date_to": None, "comments": None, "period_of_time": list_reason_typ_line.copy(),
#                'color': None, "amount_of_channels": {"КЛС": None, "ЦРРЛ": None}
#     }
#
#     for outfit in outfits:
#         total_outfit = copy.deepcopy(example)
#         total_outfit['period_of_time'] = dict.fromkeys(list_reason_typ_line, 0)
#         out_data = copy.deepcopy(example)
#         out_data['name'] = outfit.responsible_outfit.outfit
#         out_data['color'] = "1"
#         data.append(out_data)
#
#         for event in all_event_name.filter(responsible_outfit=outfit.responsible_outfit):
#             event_data = copy.deepcopy(example)
#             event_data['name'] = get_event_name(event)
#             data.append(event_data)
#             example['period_of_time'] = dict.fromkeys(list_reason_typ_line, 0)
#             total_period_of_time = copy.deepcopy(example)
#
#             for call in get_calls_list(all_event, event):
#                 period = get_period(call, date_to)
#
#                 if call.ips is None:
#                     type_line = get_type_line(call)
#                     amount_of_channels = get_amount_of_channels(call)
#
#                     call_data = copy.deepcopy(example)
#                     call_data['date_from'] = call.date_from
#                     call_data['date_to'] = call.date_to
#                     call_data['period_of_time'][call.reason.name+type_line] = period
#
#                     call_data['amount_of_channels'][type_line] = amount_of_channels
#                     call_data['comments'] = call.comments1
#
#                     total_period_of_time['period_of_time'][call.reason.name+type_line] += period
#
#                     data.append(call_data)
#                 else:
#                     call_data = copy.deepcopy(example)
#                     call_data['date_from'] = call.date_from
#                     call_data['date_to'] = call.date_to
#                     call_data['comments'] = call.comments1
#                     kls = call.ips.total_point_channels_KLS
#                     rrl = call.ips.total_point_channels_RRL
#
#                     if kls != 0:
#                         call_data['amount_of_channels']["КЛС"] = kls
#                         call_data['period_of_time'][call.reason.name + 'КЛС'] = period
#                         total_period_of_time['period_of_time'][call.reason.name + 'КЛС'] += period
#
#                     if rrl != 0:
#                         call_data['amount_of_channels']["ЦРРЛ"] = rrl
#                         call_data['period_of_time'][call.reason.name + 'ЦРРЛ'] = period
#                         total_period_of_time['period_of_time'][call.reason.name + 'ЦРРЛ'] += period
#                     data.append(call_data)
#
#
#             total = dict(total_period_of_time)
#             if event.ips is None:
#                 for i in total['period_of_time']:
#                     total['period_of_time'][i] = round(total['period_of_time'][i] * int(get_amount_of_channels(event)), 2)
#                     total_outfit['period_of_time'][i] += total['period_of_time'][i]
#             else:
#                 k = event.ips.total_point_channels_KLS
#                 r = event.ips.total_point_channels_RRL
#
#                 for i in total['period_of_time']:
#                     if k != 0:
#                         total['period_of_time'][i] = round(total['period_of_time'][i] * k, 2)
#                         total_outfit['period_of_time'][i] += total['period_of_time'][i]
#                     if r != 0:
#                         total['period_of_time'][i] = round(total['period_of_time'][i] * r, 2)
#                         total_outfit['period_of_time'][i] += total['period_of_time'][i]
#
#             total_period_of_time['name'] = 'всего'
#             total_period_of_time['date_from'] = 'час'
#             total_period_of_time['color'] = '2'
#             data.append(total_period_of_time)
#             total['name'] = 'всего'
#             total['date_from'] = 'кнл/час'
#             total['color'] = '3'
#             data.append(total)
#
#         total_outfit['name'] = 'Общий итог'
#         total_outfit['color'] = '4'
#         data.append(total_outfit)
#     return JsonResponse(data, safe=False)



class AmountChannelsObjectKLSRRLAPIView(UpdateAPIView):
    '''сохранение количества каналов для Обьекта'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = AmountChannelsKLSRRL.objects.all()
    serializer_class = AmountChannelsKLSRRLSerializer



@permission_classes([IsAuthenticated, SuperUser|IsAKOnly])
def get_report(request):
    """ Форма анализа"""
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    responsible_outfit = request.GET.getlist("responsible_outfit")


    all_event = Event.objects.filter(index1__index='1', callsorevent=False, reason__name__in=['Откл. ЭЭ', 'ПВ аппаратуры',
                                                                                              'Линейные ПВ', 'Хищения на ЛС', 'ПВ за счет стихии']).exclude(name__isnull=False)

    all_event = event_filter_date_from_date_to_and_outfit(all_event, date_from, date_to, responsible_outfit)

    all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")
    outfits = event_distinct(all_event, "responsible_outfit")

    data = []

    list_reason_typ_line = {
        "Откл. ЭЭКЛС": None, "Откл. ЭЭЦРРЛ": None, "ПВ аппаратурыКЛС": None,
        "ПВ аппаратурыЦРРЛ": None, "Линейные ПВКЛС": None, "Линейные ПВЦРРЛ": None,
        "Хищения на ЛСКЛС": None, "Хищения на ЛСЦРРЛ": None, "ПВ за счет стихииКЛС": None, 'ПВ за счет стихииЦРРЛ': None
        }

    example = {'id': None, "name": None, "date_from": None, "date_to": None, "comments": None, "period_of_time": list_reason_typ_line.copy(),
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
            amount_channels_id, amount_channels_KLS, amount_channels_RRL = get_amount(event)
            event_data = copy.deepcopy(example)
            event_data['name'] = get_event_name(event)
            event_data['id'] = amount_channels_id
            data.append(event_data)
            example['period_of_time'] = dict.fromkeys(list_reason_typ_line, 0)
            total_period_of_time = copy.deepcopy(example)

            for call in get_calls_list(all_event, event):
                period = get_period(call, date_to)
                call_data = copy.deepcopy(example)
                call_data['date_from'] = call.date_from
                call_data['date_to'] = call.date_to
                if amount_channels_KLS != 0:
                    call_data['period_of_time'][call.reason.name+'КЛС'] = period
                    total_period_of_time['period_of_time'][call.reason.name + 'КЛС'] += period

                if amount_channels_RRL != 0:
                    call_data['period_of_time'][call.reason.name+'ЦРРЛ'] = period
                    total_period_of_time['period_of_time'][call.reason.name + 'ЦРРЛ'] += period

                call_data['amount_of_channels']['КЛС']= amount_channels_KLS
                call_data['amount_of_channels']['ЦРРЛ'] = amount_channels_RRL
                call_data['comments'] = call.comments1
                data.append(call_data)
            total_period_of_time['name'] = 'всего'
            total_period_of_time['date_from'] = 'час'
            total_period_of_time['color'] = '2'
            data.append(total_period_of_time)
            total = copy.deepcopy(total_period_of_time)
            for i in total['period_of_time']:
                if amount_channels_KLS != 0:
                    total['period_of_time'][i] = round(total['period_of_time'][i] * amount_channels_KLS, 2)
                    total_outfit['period_of_time'][i] += total['period_of_time'][i]
                if amount_channels_RRL != 0:
                    total['period_of_time'][i] = round(total['period_of_time'][i] * amount_channels_RRL, 2)
                    total_outfit['period_of_time'][i] += total['period_of_time'][i]

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

    all_events = Event.objects.filter(callsorevent=False).exclude(name__isnull=False).exclude(index1__index='4')

    if index is not None and index != "":
        all_events = all_events.filter(index1__id=index)

    all_events= event_filter_date_from_date_to_and_outfit(all_events, date_from, date_to, responsible_outfit)

    all_event_names = all_events.order_by('ips_id', 'object_id', 'circuit_id').distinct('ips_id', 'object_id',
                                                                                                'circuit_id')
    outfits = all_event_names.order_by("responsible_outfit").distinct("responsible_outfit")

    data = []

    example = {"outfit": None, 'id': None, "name": None, "reason": None,
               "date_from": None,  "date_to": None, 'region': None,
               "index1": None, "comments1": None}

    for out in outfits:
        out_data = example.copy()
        out_data['outfit'] = out.responsible_outfit.outfit
        data.append(out_data)
        for event in all_event_names.filter(responsible_outfit=out.responsible_outfit):
            event_data = example.copy()
            event_data['id'] = event.id
            event_data['name'] = get_event_name(event)
            data.append(event_data)

            for call in all_events.filter(object=event.object, ips=event.ips, circuit=event.circuit).order_by('date_from'):
                call_data = example.copy()
                call_data['id'] = None
                call_data['name'] = '-'
                call_data['reason'] = call.reason.name
                call_data['date_from'] = call.date_from
                call_data['date_to'] = get_date_to_ak(call, date_to) if date_from is not None and  date_to is  not None else get_date_to(call, date_to if date_to is not None else date_from)
                call_data['region'] = call.point1.point + " - " + call.point2.point if call.point1 is not None else ""
                call_data['comments1'] = call.comments1
                call_data['index1'] = call.index1.index
                data.append(call_data)

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
        form_list = FormAnalysis.objects.filter(id_parent=self.get_object().pk).order_by('outfit')
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
    order_by = 'outfit'


class Punkt7ListAPIView(APIView, ListWithPKMixin):
    """Список п.5"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)
    model = Punkt7
    serializer = Punkt7ListSerializer
    field_for_filter = "form_analysis__id_parent"
    order_by = 'outfit'


class Punkt5UpdateAPIView(generics.UpdateAPIView):
    """Редактирование п.5"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly, IngenerUser)
    lookup_field = "pk"
    queryset = Punkt5.objects.all()
    serializer_class = Punkt5UpdateSerializer

    def perform_update(self, serializer):
        punkt5 = serializer.save()
        update_punkt5(punkt5, self.request.data["total_coefficient"])


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
        punkt7 = serializer.save()
        update_punkt7(punkt7)


class Punkt7DeleteAPIView(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly, IngenerUser)
    queryset = Punkt7.objects.all()
    lookup_field = "pk"

    def perform_destroy(self, instance):
        delete_punkt7(instance)


class ReportOaAndOdApiView(APIView):
    """Отчет по Од, Оа"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)

    def get(self, request):
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        responsible_outfit = request.GET.getlist("responsible_outfit")
        index = request.GET.get("index")

        od = Index.objects.get(index="0д")
        oa = Index.objects.get(index="0а")

        if index is None or index == '':
            all_event = Event.objects.filter(index1__in=[od, oa],  callsorevent=False).exclude(name__isnull=False)
        elif index in [str(od.id), str(oa.id)]:
            all_event = Event.objects.filter(index1=index,
                                         callsorevent=False).exclude(name__isnull=False)
        else:
            data = {'detail': "Можно фильтровать только по индексу Од, Оа"}
            return Response(data, status.HTTP_403_FORBIDDEN)

        all_event = event_filter_date_from_date_to_and_outfit(all_event, date_from, date_to, responsible_outfit)
        outfits = event_distinct(all_event, "responsible_outfit")
        all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")
        data = []

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
            "total_sum": {"sum": 0, "count": 0}

        }

        for out in outfits:
            outfit = out.responsible_outfit
            data.append({"outfit": outfit.outfit, "name": None, "total_sum": {"sum": None, "count": None}, "oa": {"sum": None, "count": None}, "od": {"sum": None, "count": None}})
            outfit_data = {"outfit": outfit.outfit, "name": None, "total_sum": {"sum": 0, "count": 0}, "oa": {"sum": 0, "count": 0}, "od": {"sum": 0, "count": 0}}
            for event in all_event_name.filter(responsible_outfit=outfit):
                count_od = get_count_event(all_event, event, od, outfit)
                count_oa = get_count_event(all_event, event, oa, outfit)

                sum_oa = get_sum_period_of_time_event(all_event, event, oa, outfit, date_to)
                sum_od = get_sum_period_of_time_event(all_event, event, od, outfit, date_to)

                winner_index = len(data)
                winners_oa = determine_the_winner(winners_oa, sum_oa, winner_index)
                winners_od = determine_the_winner(winners_od, sum_od, winner_index)

                data.append({"name": get_event_name(event), "outfit": None,
                                       "total_sum": {"sum": sum_oa+sum_od, "count": count_oa + count_od, "color": None},
                                       "oa": {"sum": sum_oa, "count": count_oa, "color": None},
                                       "od": {"sum": sum_od, "count": count_od, "color": None}})
                outfit_data["oa"]["count"] += count_oa
                outfit_data["od"]["count"] += count_od
                outfit_data["oa"]["sum"] += round(sum_oa, 2)
                outfit_data["od"]["sum"] += sum_od

                outfit_data['total_sum']['sum'] = outfit_data["oa"]["sum"] + outfit_data["od"]["sum"]
                outfit_data['total_sum']['count'] = outfit_data["oa"]["count"] + outfit_data["od"]["count"]

            rep["oa"]["count"] +=  outfit_data["oa"]["count"]
            rep["od"]["count"] +=  outfit_data["od"]["count"]

            rep["oa"]["sum"] += outfit_data["oa"]["sum"]
            rep["od"]["sum"] += outfit_data["od"]["sum"]

            rep['total_sum']['sum'] = rep["oa"]["sum"] + rep["od"]["sum"]
            rep['total_sum']['count'] = rep["oa"]["count"]+rep["od"]["count"]
            winners_oa = set_response_for_winners(winners_oa, "oa", data)
            winners_od = set_response_for_winners(winners_od, "od", data)

            data.append(outfit_data)
        rep["oa"]["sum"] = round(rep["oa"]["sum"], 2)
        rep["od"]["sum"] = round(rep["od"]["sum"], 2)

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

            list_index = [oa, od]
        else:
            list_index = [Index.objects.get(pk=index_id)]

        all_event = Event.objects.filter(index1__in=list_index, callsorevent=False).exclude(name__isnull=False)
        all_event = event_filter_date_from_date_to_and_outfit(all_event, date_from, date_to, responsible_outfit)
        outfits = event_distinct(all_event, "responsible_outfit")
        all_event_name = event_distinct(all_event, "ips_id", "object_id", "circuit_id")
        winners = {i.index: [{"name": None, "sum": 0, "count": 0} for _ in range(3)] for i in list_index}
        data = []

        for out in outfits:
            outfit = out.responsible_outfit
            for index in list_index:
                for event in all_event_name.filter(responsible_outfit=outfit, index1=index):
                    sum = get_sum_period_of_time_event(all_event, event, index, outfit, date_to)
                    count = get_count_event(all_event, event, index, outfit)
                    event_name = get_event_name(event)
                    get_winners(winners[index.index], event_name, sum, count)

                data.append({"outfit": outfit.outfit, "index": index.index, "winners": winners[index.index]})

        return JsonResponse(data, safe=False)

class Form61KLSCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)

    def post(self, request):
        serializer = Form61KLSCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Form61KLSList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)

    def get(self, request):
        outfit = self.request.query_params.get('outfit', None)
        type_connection = self.request.query_params.get('type_connection', None)
        queryset = Form61KLS.objects.all().order_by('type_connection').prefetch_related('outfit', 'point1', 'point2', 'type_cable', 'type_connection')
        if outfit is not None and outfit != "":
            queryset = queryset.filter(outfit_id=outfit)
        if type_connection is not None and type_connection != "":
            queryset = queryset.filter(type_connection=type_connection)
        serializer = Form61KLSSerializer(queryset, many=True)
        return Response(serializer.data)

class Form61KLSUpdateAPIView(UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)
    queryset = Form61KLS.objects.all()
    serializer_class = Form61KLSCreateSerializer

@permission_classes([IsAuthenticated, SuperUser|IsAKOnly])
def get_report_form61_kls(request):
    """ Форма61 KLS"""
    outfit = request.GET.getlist("outfit")
    type_connection = request.GET.get("type_connection")
    forms61 = Form61KLS.objects.all()
    all_form61 = form61_kls_filter(forms61, outfit, type_connection)
    outfits = form61_kls_distinct(all_form61, "outfit")
    data = []
    content = {'id': None, "name": None, "year_of_laying": None, "type_cable": None, "total_length_line": 0,
               'total_length_cable': 0, "laying_method": None, 'color':None
    }
    total_rep = copy.deepcopy(content)
    for outfit in outfits:
        total_outfit = copy.deepcopy(content)
        out_data = copy.deepcopy(content)
        out_data['name'] = outfit.outfit.outfit
        out_data['color'] = "1"
        data.append(out_data)
        for form61 in all_form61.filter(outfit=outfit.outfit):
            form61_data = copy.deepcopy(content)
            form61_data['id'] = form61.id
            form61_data['name'] = str(form61.point1.point), str(form61.point2.point)
            form61_data['year_of_laying'] = form61.year_of_laying
            form61_data['type_cable'] = form61.type_cable
            form61_data['total_length_line'] = form61.total_length_line
            form61_data['total_length_cable'] = form61.total_length_cable
            form61_data['laying_method'] = form61.laying_method.name if form61.laying_method.name is not None else ""
            data.append(form61_data)
            total_outfit['total_length_line'] += round(form61_data['total_length_line'], 2)
            total_outfit['total_length_cable'] += round(form61_data['total_length_cable'], 2)
        total_outfit['name'] = 'ИТОГО:'
        total_outfit['color'] = '2'
        data.append(total_outfit)
        total_rep['total_length_line'] += round(total_outfit['total_length_line'], 2)
        total_rep['total_length_cable'] += round(total_outfit['total_length_cable'], 2)
    total_rep['name'] = 'ИТОГО:'
    total_rep['color'] = '3'
    data.append(total_rep)
    return JsonResponse(data, safe=False)

from io import BytesIO

def get_distance_length_kls(request, pk1, pk2):
    point1 = get_object_or_404(Point, pk=pk1)
    point2 = get_object_or_404(Point, pk=pk2)
    g = nx.Graph()
    g2 = nx.Graph()
    data = []
    content = {'name':None, 'points': None, 'sum_line':0, "sum_cable": 0, 'src':None}

    for form in Form61KLS.objects.all():
        g.add_edge(form.point1.point, form.point2.point, weight=form.total_length_line)
        g2.add_edge(form.point1.point, form.point2.point, weight=form.total_length_cable)
        g.add_node(form.point1.point, pos=(1, 20))
        g.add_node(form.point2.point, pos=(1, 20))
    pos = nx.spring_layout(g)
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)
    nx.draw(g, pos, with_labels=True)
    src = BytesIO()
    plt.savefig('graph', format='png')

    # content_file = ContentFile(f.getvalue())
    # model_object = Form61KLS
    # model_object.src.save('graph', content_file)
    # model_object.save()




    path = []
    for p in nx.all_simple_paths(g, source=point1.point, target=point2.point):
        path.append(p)
    for p in path:
        path_length = nx.path_weight(g, p, weight='weight')
        path_length1 = nx.path_weight(g2, p, weight='weight')
        finish_total = copy.deepcopy(content)
        finish_total['name'] = "Варианты:"
        finish_total['points'] = p
        finish_total['sum_line'] = path_length
        finish_total['sum_cable'] = path_length1
        data.append(finish_total)
    for p in nx.all_simple_edge_paths(g, source=point1.point, target=point2.point):
        for t in p:
            total = copy.deepcopy(content)
            total['name'] = "Разбивка:"
            total['points'] = t
            path_length = nx.path_weight(g, t, weight='weight')
            path_length1 = nx.path_weight(g2, t, weight='weight')
            total['sum_line'] = path_length
            total['sum_cable'] = path_length1
            data.append(total)

    return JsonResponse(data, safe=False)

class TypeConnectionViewSet(viewsets.ModelViewSet):
    queryset = TypeConnection.objects.all().order_by('-id')
    serializer_class = TypeConnectionSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = "pk"
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)


class MethodLayingViewSet(viewsets.ModelViewSet):
    queryset = MethodLaying.objects.all().order_by('-id')
    serializer_class = MethodLayingSerializer
    authentication_classes = (TokenAuthentication,)
    lookup_field = "pk"
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)


class TypeCableViewSet(ModelViewSet):
    queryset = TypeCable.objects.all()
    serializer_class = TypeCableSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,  SuperUser|IsAKOnly)


