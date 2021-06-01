
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView
from apps.opu.form51.models import Form51
from apps.opu.form51.serializers import Form51CreateSerializer, Form51Serializer
from apps.accounts.permissions import IsPervichkaOnly, SuperUser, IngenerUser
from apps.opu.form51.service import get_form51_diff


class FormListAPIView(ListAPIView):
    """Список Формы 5.1"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Form51Serializer

    def get_queryset(self):
        queryset = Form51.objects. \
            defer('created_by', 'object__tpo1', 'object__tpo2', 'object__point1',
                  'object__point2', 'object__id_parent', 'object__amount_channels', 'object__created_by',
                  'object__customer', 'object__type_line', 'object__type_of_trakt'). \
            select_related('customer', 'object').prefetch_related('object__bridges__transit__trassa')
        outfit = self.request.query_params.get('outfit', None)
        customer = self.request.query_params.get('customer', None)
        object = self.request.query_params.get('object', None)
        consumer = self.request.query_params.get('consumer', None)

        if outfit is not None:
            queryset = queryset.filter(object__id_outfit=outfit)
        if customer is not None:
            queryset = queryset.filter(customer=customer)
        if object is not None:
            queryset = queryset.filter(object=object)
        if consumer is not None and consumer != '':
            queryset = queryset.filter(object__consumer=consumer)
        return queryset


class Form51UpdateAPIView(UpdateAPIView):
    """Редактирования Формы 5.1"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    queryset = Form51.objects.all()
    serializer_class = Form51CreateSerializer


class Form51History(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly, )

    def get(self, request, pk):
        form51 = Form51.objects.get(pk=pk)
        histories = form51.history.all()
        data = []
        for h in histories:
            a = {}
            a['history_id'] = h.history_id
            a['updated_date'] = h.history_date
            a['updated_by'] = h.history_user.username
            a['change_method'] = h.get_history_type_display()
            a['changes'] = get_form51_diff(history=h)
            if a['changes'] == "" and h.history_type =='~':
                continue
            data.append(a)
        return Response(data, status=status.HTTP_200_OK)