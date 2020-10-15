from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from knox.auth import TokenAuthentication
import datetime

from apps.analysis.models import FormAnalysis, Item5, OutfitItem5, SpecificGravityOfLength, \
    SpecificGravityOfLengthTypeLine, Item7
from apps.analysis.serializers import DispEvent1ListSerializer, FormAnalysisSerializer, \
    FormAnalysisDetailSerializer, OutfitItem5ListSerializer, Item5UpdateSerializer, \
    Item5CreateSerializer, Item7CreateSerializer, Item7UpdateSerializer
from django.http import JsonResponse

from apps.analysis.service import get_period, get_type_line, get_calls_list, get_amount_of_channels, \
    create_item5, update_item5, update_downtime_and_coefficient, update_total_length, \
    update_total_length_and_total_coefficient, create_spec_type_line, check_object, get_parent_item5, \
    sum_total_coefficient, item5_delete, update_item7_coefficient_and_match_percentage, \
    update_total_coefficient_and_total_length_item7, update_item7, item7_delete, update_form_coefficient, \
    update_outfit_period_of_time_and_length_republic, update_total_object_and_corresponding_norm

from apps.dispatching.models import Event, HistoricalEvent
from apps.dispatching.services import get_event_name
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
import threading

from apps.opu.services import ListWithPKMixin


def get_report(request):
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    responsible_outfit = request.GET.get("responsible_outfit")

    all_event = Event.objects.filter(index1_id=3, callsorevent=False)

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
        total_outfit = {"name1": 0, "name2": 0, "name3": 0, "name4": 0, 'name5':0, 'name6':0, 'name7':0, 'name8':0 }
        data.append({
            "name": outfit.responsible_outfit.outfit,
            "date_from": None, "comments": None,
            "reason": None, "type_line": None, "color":'1',
            "period_of_time": {"name1": None, "name2": None, "name3": None,
                               "name4": None, "name5":None, "name6":None }, "amount_of_channels": None
        })
        for event in all_event_name.filter(responsible_outfit=outfit.responsible_outfit):
            data.append({
                "name": get_event_name(event),
                "date_from": None, "comments": None,
                "reason": None, "type_line": None,
                "period_of_time": {"name1": None, "name2": None, "name3": None,
                                   "name4": None, "name5":None, "name6":None},
                "amount_of_channels": None
            })
            total_period_of_time = {"name1": 0, "name2": 0, "name3": 0, "name4": 0,
                                    'name5':0, 'name6':0, 'name7':0, 'name8':0}


            for call in get_calls_list(all_event, event):
                period = get_period(call, date_to)
                type_line = get_type_line(call)
                amount_of_channels = get_amount_of_channels(call)
                period_reason = {"name1": None, "name2": None, "name3": None, "name4": None,
                                 "name5":None, "name6":None, "name7":None, "name8":None}
                if call.reason.id == 1 and type_line == 1:
                    total_period_of_time["name1"] += period
                    period_reason["name1"] = period
                elif call.reason.id ==1 and type_line ==2:
                    total_period_of_time["name2"] += period
                    period_reason["name2"] = period
                elif call.reason.id == 2 and type_line==1:
                    total_period_of_time["name3"] += period
                    period_reason["name3"] = period
                elif call.reason.id == 2 and type_line==2:
                    total_period_of_time["name4"] += period
                    period_reason["name4"] = period
                elif call.reason.id == 3 and type_line == 1:
                    total_period_of_time["name5"] += period
                    period_reason["name5"] = period
                elif call.reason.id == 3 and type_line == 2:
                    total_period_of_time["name6"] += period
                    period_reason["name6"] = period
                elif call.reason.id == 4 and type_line ==1:
                    total_period_of_time["name7"] += period
                    period_reason["name7"] = period
                elif call.reason.id == 4 and type_line ==2:
                    total_period_of_time["name8"] += period
                    period_reason["name8"] = period

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
    queryset = Event.objects.filter(callsorevent=False, index1__id=3)
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


# class DispEventHistory(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticatedOrReadOnly,)
#     authentication_classes = (TokenAuthentication,)
#     queryset = HistoricalEvent.objects.all()
#     lookup_field = 'pk'
#     serializer_class = HistoryEventSerializer


class CreateFormAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        date_to = request.data["date_to"]
        date_from = request.data["date_from"]
        outfit = request.data["outfit"]
        func = threading.Thread(target=create_item5(), args=(date_to, date_from, outfit))
        func.start()
        data = {"response": "Отчет успешно создан"}
        return Response(data, status=status.HTTP_200_OK)


class DispEventHistory(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        histories = event.history_log.filter(id=pk)
        old = histories.first()
        new = histories.last()
        delta = new.diff_against(old)
        for change in delta.changes:
            text = ("{} изменился от {} к {}".format(change.field, change.old, change.new))
        data = []
        for history in histories:
            h = {}
            h['id']=history.history_id
            h['date'] = history.history_date
            h['user'] = history.history_user.username
            h['type'] = history.history_type
            h['object'] = history.history_object.id
            if history.history_type is '~':
                h['changed_field'] = str(text)
            elif history.history_type is '+':
                h['changed_field'] = str("Создан обьект")
            elif history.history_type is '-':
                h['changed_field'] = str("Удален обьект")
            data.append(h)
        return Response(data, status=status.HTTP_200_OK)


class FormAnalysisAPIViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = FormAnalysis.objects.filter(id_parent=None)
    serializer_class = FormAnalysisSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FormAnalysisDetailSerializer
        return FormAnalysisSerializer

    def perform_create(self, serializer):
        """Создание парентев для обектов"""
        total_for_item5 = SpecificGravityOfLength.objects.create()
        total_for_item7 = SpecificGravityOfLength.objects.create()
        type_line = SpecificGravityOfLengthTypeLine.objects.create(specific_gravity_of_length=total_for_item5,
                                                                   type_line_id=1)
        type_line7 = SpecificGravityOfLengthTypeLine.objects.create(specific_gravity_of_length=total_for_item7,
                                                                    type_line_id=1)
        item5out = OutfitItem5.objects.create(total_coefficient=total_for_item5)
        item7out = OutfitItem5.objects.create(total_coefficient=total_for_item7)
        item5out.id_parent = item5out
        item5out.save()
        item7out.id_parent = item7out
        item7out.save()
        form = serializer.save(user=self.request.user.profile, coefficient_item5=item5out, coefficient_item7=item7out)
        Item5.objects.create(date_from=form.date_from, date_to=form.date_to, outfit_item5=item5out, type_line_id=1,
                             type_line_value=type_line)
        Item7.objects.create(date_from=form.date_from, date_to=form.date_to, outfit_item5=item7out, type_line_id=1,
                             type_line_value=type_line7)

    def retrieve(self, request, *args, **kwargs):
        """ Список ср.КФТ отчет """
        form_list = FormAnalysis.objects.filter(id_parent=self.get_object().pk)
        serializer = self.get_serializer(form_list, many=True)
        return Response(serializer.data)


class FormAnalysisCreateAPIViewItem5(APIView):
    """ Создание ср.КФТ отчета """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        date_from = request.data["date_from"]
        date_to = request.data["date_to"]
        outfit = request.data["outfit"]
        parent = FormAnalysis.objects.get(pk=pk)
        create_item5(date_from, date_to, outfit, parent)
        data = {"response": "Успешно создан"}
        return Response(data, status=status.HTTP_201_CREATED)


class OutfitItem5ListAPIView(APIView, ListWithPKMixin):
    """Список п.5"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = OutfitItem5
    serializer = OutfitItem5ListSerializer
    field_for_filter = "id_parent"


class Item5UpdateAPIView(generics.UpdateAPIView):
    """Редактирование п.5"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"
    queryset = Item5.objects.all()
    serializer_class = Item5UpdateSerializer

    def perform_update(self, serializer):
        item5 = serializer.save()
        update_item5(new_item5=item5)  # обновление п.5


class Item5CreateAPIView(APIView):
    """Создание п.5"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        out_item5 = OutfitItem5.objects.get(pk=pk)
        serializer = Item5CreateSerializer(data=request.data)
        if serializer.is_valid():
            item5 = serializer.save(outfit_item5=out_item5)
            update_downtime_and_coefficient(item5)
            update_total_length_and_total_coefficient(out_item5)
            create_spec_type_line(out_item5, item5)
            ############################################################
            if check_object(out_item5, item5):
                parent_item5 = get_parent_item5(out_item5, item5)
                update_outfit_period_of_time_and_length_republic(parent_item5.outfit_item5, parent_item5)
                update_downtime_and_coefficient(parent_item5)
                update_total_length(out_item5.id_parent)
                sum_total_coefficient(out_item5.id_parent)
            else:
                rep_item5 = Item5.objects.create(outfit_item5=out_item5.id_parent,
                                                 type_line=item5.type_line, length=item5.length,
                                                 outfit_period_of_time=item5.outfit_period_of_time)
                update_downtime_and_coefficient(rep_item5)
                update_total_length(out_item5.id_parent)
                create_spec_type_line(out_item5.id_parent, rep_item5)
                sum_total_coefficient(out_item5.id_parent)
                update_form_coefficient(out_item5.id_parent.form_item5)

            update_form_coefficient(out_item5.form_item5)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Item5DeleteAPIVIew(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Item5.objects.all()

    def perform_destroy(self, instance):
        item5_delete(instance)


class Item7CreateAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        out_item5 = OutfitItem5.objects.get(pk=pk)
        serializer = Item7CreateSerializer(data=request.data)
        if serializer.is_valid():
            item7 = serializer.save(outfit_item5=out_item5)
            update_item7_coefficient_and_match_percentage(item7)
            update_total_coefficient_and_total_length_item7(out_item5)
            create_spec_type_line(out_item5, item7, item7=True)
            if check_object(out_item5, item7, item7=True):
                parent_item7 = get_parent_item5(out_item5, item7, item7=True)
                update_total_object_and_corresponding_norm(out_item5.id_parent, parent_item7)
                update_item7_coefficient_and_match_percentage(parent_item7)
                update_total_coefficient_and_total_length_item7(parent_item7.outfit_item5)
            else:
                rep_item7 = Item7.objects.create(outfit_item5=out_item5.id_parent, type_line=item7.type_line,
                                                 total_object=item7.total_object,
                                                 corresponding_norm=item7.corresponding_norm)
                update_item7_coefficient_and_match_percentage(rep_item7)
                create_spec_type_line(out_item5.id_parent, rep_item7, item7=True)
                update_total_coefficient_and_total_length_item7(rep_item7.outfit_item5)
                update_form_coefficient(out_item5.id_parent.form_item7)

            update_form_coefficient(out_item5.form_item7)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Item7UpdateAPIView(generics.UpdateAPIView):
    """Редактирование п.7"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = "pk"
    queryset = Item7.objects.all()
    serializer_class = Item7UpdateSerializer

    def perform_update(self, serializer):
        item7 = serializer.save()
        update_item7(item7)


class Item7DeleteAPIView(generics.DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Item7.objects.all()

    def perform_destroy(self, instance):
        item7_delete(instance)
