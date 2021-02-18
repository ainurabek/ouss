# coding: utf-8
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from rest_framework import status
from django.db.models import Q
from apps.accounts.permissions import IsPervichkaOnly
from apps.opu.circuits.serializers import CircuitTrassaList
from apps.opu.form_customer.models import Form_Customer
from apps.opu.objects.serializers import PGListSerializer
from apps.opu.circuits.models import Circuit
from apps.opu.circuits.serializers import CircuitList
from apps.opu.objects.models import Object, Point
from apps.opu.objects.serializers import SelectObjectSerializer, PointList, ObjectListSerializer


class SelectObjectView(APIView):
    """Выбор ЛП для создания трассы"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

    def get(self, request, pk):
        obj = Object.objects.get(pk=pk)
        serializer = SelectObjectSerializer(obj).data
        return Response(serializer)


class PointListTrassa(ListAPIView):
    """Список ИП для создания трассы"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Point.objects.all().order_by('point').values('id', 'point')
    serializer_class = PointList


class SelectPointView(APIView):
    """Выбор ИП для фильтрацы ЛП"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        point = Point.objects.get(pk=pk)
        lps = Object.objects.filter(Q(point1=point) | Q(point2=point), id_parent=None)
        serializer = ObjectListSerializer(lps, many=True).data
        return Response(serializer)


class ObjectList(APIView):
    """Список ПГ, ВГ итд"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        obj = Object.objects.get(pk=pk)
        childs = obj.parents.all()
        serializer = ObjectListSerializer(childs, many=True).data
        return Response(serializer)


class CreateLeftTrassaView(APIView):
    permission_classes = (IsAuthenticated, IsPervichkaOnly)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, main_pk, pk):
        main_obj = Object.objects.get(pk=main_pk)
        obj = Object.objects.get(pk=pk)

        if not main_obj.transit.filter(pk=pk).exists():
            main_obj.transit.add(*obj.transit2.all().reverse(), *obj.transit.all())

            for tr in obj.transit.all():
                tr.transit2.clear()
                tr.transit.clear()
            for tr in obj.transit2.all():
                tr.transit2.clear()
                tr.transit.clear()

            Object.objects.filter(pk=pk).update(created_by=request.user.profile)

            num_circuit = main_obj.circuit_object_parent.count() if main_obj.circuit_object_parent.count() \
                                                                    <= obj.circuit_object_parent.count() else \
                obj.circuit_object_parent.count()
            if num_circuit != 0:

                for cir in main_obj.circuit_object_parent.all():
                    if int(cir.num_circuit) > num_circuit:
                        break
                    circuit = obj.circuit_object_parent.all()[int(cir.num_circuit)-1]
                    cir.transit.add(*circuit.transit.all(), *circuit.transit2.all())
                    for tr in circuit.transit.all():
                        tr.transit2.clear()
                        tr.transit.clear()
                    for tr in circuit.transit2.all():
                        tr.transit2.clear()
                        tr.transit.clear()

        response = {"data": "Объект успешно добавлен в трассу"}
        return Response(response, status=status.HTTP_201_CREATED)


class CreateRightTrassaView(APIView):
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, main_pk, pk):
        main_obj = Object.objects.get(pk=main_pk)
        obj = Object.objects.get(pk=pk)
        # if main_pk.is_transit is True or obj.is_transit is True:
        #     message = {"detail": "Создание трассы может привести к перезаписи трассы транзитных каналов"}
        #     return Response(message, status=status.HTTP_403_FORBIDDEN)
        if not main_obj.transit2.filter(pk=pk).exists():
            main_obj.transit2.add(*obj.transit.all().reverse(), *obj.transit2.all())
            for tr in obj.transit.all():
                tr.transit2.clear()
                tr.transit.clear()
            for tr in obj.transit2.all():
                tr.transit2.clear()
                tr.transit.clear()
            Object.objects.filter(pk=pk).update(created_by=request.user.profile)

            num_circuit = main_obj.circuit_object_parent.count() if main_obj.circuit_object_parent.count() <=\
                                                                    obj.circuit_object_parent.count() else\
                obj.circuit_object_parent.count()

            if num_circuit != 0:
                for cir in main_obj.circuit_object_parent.all():
                    if int(cir.num_circuit) > num_circuit:
                        break
                    circuit = obj.circuit_object_parent.all()[int(cir.num_circuit)-1]
                    cir.transit2.add(*circuit.transit.all(), *circuit.transit2.all())
                    for tr in circuit.transit.all():
                        tr.transit2.clear()
                        tr.transit.clear()
                    for tr in circuit.transit2.all():
                        tr.transit2.clear()
                        tr.transit.clear()
        response = {"data": "Объект успешно добавлен в трассу"}
        return Response(response, status=status.HTTP_201_CREATED)


class SaveTrassaView(APIView):
    """Сохранение трассы"""
    authentication_classes = (TokenAuthentication, IsPervichkaOnly,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        main_obj = get_object_or_404(Object, pk=pk)
        for i in main_obj.transit.all():
            i.transit.add(*main_obj.transit.all())
            i.transit2.add(*main_obj.transit2.all())

        for i in main_obj.transit2.all():
            i.transit2.add(*main_obj.transit2.all())
            i.transit.add(*main_obj.transit.all())

        for cir in main_obj.circuit_object_parent.all():
            for obj in main_obj.transit.all():
                if obj.circuit_object_parent.count() == 0:
                    continue
                try:
                    circuit = obj.circuit_object_parent.all()[int(cir.num_circuit)-1]
                except IndexError:
                    break
                circuit.transit.add(*cir.transit.all())
                circuit.transit2.add(*cir.transit2.all())

        for cir in main_obj.circuit_object_parent.all():
            for obj in main_obj.transit2.all():
                if obj.circuit_object_parent.count() == 0:
                    continue
                try:
                    circuit = obj.circuit_object_parent.all()[int(cir.num_circuit)-1]
                except IndexError:
                    break
                circuit.transit2.add(*cir.transit2.all())
                circuit.transit.add(*cir.transit.all())

        return Response(status=status.HTTP_201_CREATED)

    def post(self, request, pk):
        main_obj = Object.objects.get(pk=pk)
        data = request.data
        if data['customer'] == True:
            if Form_Customer.objects.filter(object=main_obj).exists():
                return HttpResponse("В форме арендаторов уже есть такая трасса")
            else:
                Form_Customer.objects.create(object=main_obj, customer=main_obj.customer)

        return Response(status=status.HTTP_201_CREATED)


class DeleteTrassaView(APIView):
    """Удаления трассы"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

    def delete(self, request, main_pk, pk):
        if main_pk == pk:
            message = {"detail": "Невозможно удалять выбранный обьект"}
            return Response(message, status=status.HTTP_403_FORBIDDEN)

        else:
            main_obj = Object.objects.get(pk=main_pk)
            obj = Object.objects.get(pk=pk)

            obj.transit2.clear()
            obj.transit.clear()
            obj.transit.add(obj)

            for cir in obj.circuit_object_parent.all():
                cir.transit.clear()
                cir.transit.add(cir)
                cir.transit2.clear()

            main_obj.transit.remove(obj)

            for cir in main_obj.circuit_object_parent.all():
                try:
                    circuit = obj.circuit_object_parent.all()[int(cir.num_circuit)-1]
                    cir.transit.remove(circuit)
                except IndexError:
                    pass

            main_obj.transit2.remove(obj)

            for cir in main_obj.circuit_object_parent.all():
                try:
                    circuit = obj.circuit_object_parent.all()[int(cir.num_circuit)-1]
                    cir.transit2.remove(circuit)
                except IndexError:
                    pass

            for t_obj in main_obj.transit.all():
                t_obj.transit.remove(obj)
                t_obj.transit2.remove(obj)

                for circ in t_obj.circuit_object_parent.all():
                    try:
                        circuit = obj.circuit_object_parent.all()[int(circ.num_circuit)-1]
                        circ.transit.remove(circuit)
                        circ.transit2.remove(circuit)
                    except IndexError:
                        pass

            for t_obj in main_obj.transit2.all():
                t_obj.transit2.remove(obj)
                t_obj.transit.remove(obj)

                for circ in t_obj.circuit_object_parent.all():
                    try:
                        circuit = obj.circuit_object_parent.all()[int(circ.num_circuit)-1]
                        circ.transit2.remove(circuit)
                        circ.transit.remove(circuit)
                    except IndexError:
                        pass
            return Response(status=status.HTTP_204_NO_CONTENT)


'''Создание резервной трассы'''
class CreateLeftReserveTrassaView(APIView):
    permission_classes = (IsAuthenticated, IsPervichkaOnly)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, main_pk, pk):
        main_obj = Object.objects.get(pk=main_pk)
        obj = Object.objects.get(pk=pk)

        if not main_obj.reserve_transit.filter(pk=pk).exists():
            main_obj.reserve_transit.add(*obj.reserve_transit2.all().reverse(), *obj.reserve_transit.all())

            for tr in obj.reserve_transit.all():
                tr.reserve_transit2.clear()
                tr.reserve_transit.clear()
            for tr in obj.reserve_transit2.all():
                tr.reserve_transit2.clear()
                tr.reserve_transit.clear()

        response = {"data": "Объект успешно добавлен в трассу"}
        return Response(response, status=status.HTTP_201_CREATED)


class CreateRightReserveTrassaView(APIView):
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, main_pk, pk):
        main_obj = Object.objects.get(pk=main_pk)
        obj = Object.objects.get(pk=pk)

        if not main_obj.reserve_transit2.filter(pk=pk).exists():
            main_obj.reserve_transit2.add(*obj.reserve_transit.all().reverse(), *obj.reserve_transit2.all())
            for tr in obj.reserve_transit.all():
                tr.reserve_transit2.clear()
                tr.reserve_transit.clear()
            for tr in obj.reserve_transit2.all():
                tr.reserve_transit2.clear()
                tr.reserve_transit.clear()
        response = {"data": "Объект успешно добавлен в трассу"}
        return Response(response, status=status.HTTP_201_CREATED)


class SaveReserveTrassaView(APIView):
    """Сохранение reserve трассы"""
    authentication_classes = (TokenAuthentication, IsPervichkaOnly,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        main_obj = get_object_or_404(Object, pk=pk)
        for i in main_obj.reserve_transit.all():
            i.reserve_transit.add(*main_obj.reserve_transit.all())
            i.reserve_transit2.add(*main_obj.reserve_transit2.all())

        for i in main_obj.reserve_transit2.all():
            i.reserve_transit2.add(*main_obj.reserve_transit2.all())
            i.reserve_transit.add(*main_obj.reserve_transit.all())
        return Response(status=status.HTTP_201_CREATED)


class DeleteReserveTrassaView(APIView):
    """Удаления reserve трассы"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

    def delete(self, request, main_pk, pk):
        if main_pk == pk:
            message = {"detail": "Невозможно удалять выбранный обьект"}
            return Response(message, status=status.HTTP_403_FORBIDDEN)

        else:
            main_obj = Object.objects.get(pk=main_pk)
            obj = Object.objects.get(pk=pk)

            obj.reserve_transit2.clear()
            obj.reserve_transit.clear()
            obj.reserve_transit.add(obj)

            main_obj.reserve_transit.remove(obj)
            main_obj.reserve_transit2.remove(obj)

            for t_obj in main_obj.reserve_transit.all():
                t_obj.reserve_transit.remove(obj)
                t_obj.reserve_transit2.remove(obj)
            for t_obj in main_obj.reserve_transit2.all():
                t_obj.reserve_transit2.remove(obj)
                t_obj.reserve_transit.remove(obj)
            return Response(status=status.HTTP_204_NO_CONTENT)


'''Создание трассы для каналов'''
class PGCircuitListView(APIView):
    """Выбор PG для создания трассы circuits"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

    def get(self, request, pk):
        obj = Object.objects.get(pk=pk)
        childs = obj.parents.all()
        pg = []
        while childs:
            newchilds = []
            for c in childs:
                if c.type_of_trakt.name == 'ПГ':
                    pg.append(c)
                newchilds += c.parents.all()
            childs = newchilds
        serializer = PGListSerializer(pg, many=True).data
        return Response(serializer)


class SelectCircuitView(APIView):
    """Выбор каналы для фильтрацы каналов"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk):
        obj = Object.objects.get(pk=pk)
        circuits = Circuit.objects.filter(object=obj)
        serializer = CircuitTrassaList(circuits, many=True).data
        return Response(serializer)


class CircuitListTrassa(ListAPIView):
    """Список circuits для создания трассы"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = Circuit.objects.all().order_by('num_circuit')
    serializer_class = CircuitList



#создание трассы для каналов
class CreateLeftCircuitTrassaView(APIView):
    permission_classes = (IsAuthenticated, IsPervichkaOnly)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, main_pk, pk):
        main_obj = Circuit.objects.get(pk=main_pk)
        obj = Circuit.objects.get(pk=pk)

        if not main_obj.transit.filter(pk=pk).exists():
            main_obj.transit.add(*obj.transit2.all().reverse(), *obj.transit.all())
            main_obj.object.is_transit = True
            main_obj.object.save()
            obj.object.is_transit = True
            obj.object.save()
            for tr in obj.transit.all():
                tr.transit2.clear()
                tr.transit.clear()
            for tr in obj.transit2.all():
                tr.transit2.clear()
                tr.transit.clear()
        response = {"data": "Объект успешно добавлен в трассу"}
        return Response(response, status=status.HTTP_201_CREATED)


class CreateRightCircuitTrassaView(APIView):
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, main_pk, pk):
        main_obj = Circuit.objects.get(pk=main_pk)
        obj = Circuit.objects.get(pk=pk)
        if not main_obj.transit2.filter(pk=pk).exists():
            main_obj.transit2.add(*obj.transit.all().reverse(), *obj.transit2.all())
            main_obj.object.is_transit = True
            main_obj.object.save()
            obj.object.is_transit = True
            obj.object.save()
            for tr in obj.transit.all():
                tr.transit2.clear()
                tr.transit.clear()
            for tr in obj.transit2.all():
                tr.transit2.clear()
                tr.transit.clear()
        response = {"data": "Канал успешно добавлен в трассу"}
        return Response(response, status=status.HTTP_201_CREATED)


class SaveCircuitTrassaView(APIView):
    """Сохранение трассы for circuits"""
    authentication_classes = (TokenAuthentication, IsPervichkaOnly,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        main_obj = get_object_or_404(Circuit, pk=pk)
        for i in main_obj.transit.all():
            i.transit.add(*main_obj.transit.all())
            i.transit2.add(*main_obj.transit2.all())
        for i in main_obj.transit2.all():
            i.transit2.add(*main_obj.transit2.all())
            i.transit.add(*main_obj.transit.all())
        return Response(status=status.HTTP_201_CREATED)


class DeleteCircuitTrassaView(APIView):
    """Удаления трассы для канала"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly,)

    def delete(self, request, main_pk, pk):
        if main_pk == pk:
            message = {"detail": "Невозможно удалять выбранный канал"}
            return Response(message, status=status.HTTP_403_FORBIDDEN)
        else:
            main_obj = Circuit.objects.get(pk=main_pk)
            obj = Circuit.objects.get(pk=pk)
            obj.transit2.clear()
            obj.transit.clear()
            obj.transit.add(obj)
            main_trassa = [*main_obj.object.transit.all(), main_obj.object.transit2.all()]
            circ_trassa = [*[cir.object for cir in main_obj.transit.all()], *[cir.object for cir in main_obj.transit2.all()]]

            is_transit = True
            if main_trassa != circ_trassa:
                main_obj.object.is_transit = False
            main_obj.object.is_transit = is_transit
            main_obj.object.save()
            obj.object.is_transit = is_transit
            obj.object.save()
            for t_obj in main_obj.transit.all():
                t_obj.transit.remove(obj)
                t_obj.transit2.remove(obj)
                t_obj.object.is_transit = is_transit
                t_obj.object.save()
            for t_obj in main_obj.transit2.all():
                t_obj.transit2.remove(obj)
                t_obj.transit.remove(obj)
                t_obj.object.is_transit = is_transit
                t_obj.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

