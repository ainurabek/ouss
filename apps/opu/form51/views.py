from django.shortcuts import get_object_or_404
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveDestroyAPIView

from apps.opu.form51.models import Form51
from apps.opu.form51.serializers import Form51CreateSerializer, Form51Serializer, Form51ReserveSerializer
from apps.opu.objects.models import Object
from apps.opu.form51.models import SchemaPhoto, OrderPhoto
from apps.accounts.permissions import IsPervichkaOnly, SuperUser, IngenerUser
from apps.opu.services import PhotoDeleteMixin, PhotoCreateMixin, ListWithPKMixin, create_photo
from apps.opu.form51.service import get_form51_diff


class FormListAPIView(ListAPIView):
    """Список Формы 5.1"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Form51Serializer

    def get_queryset(self):
        queryset = Form51.objects.all().prefetch_related('object', 'customer', 'order_photo', 'schema_photo')
        outfit = self.request.query_params.get('outfit', None)
        customer = self.request.query_params.get('customer', None)
        object = self.request.query_params.get('object', None)

        if outfit is not None:
            queryset = queryset.filter(object__id_outfit=outfit)
        if customer is not None:
            queryset = queryset.filter(customer=customer)
        if object is not None:
            queryset = queryset.filter(object=object)

        return queryset


class Form51UpdateAPIView(UpdateAPIView):
    """Редактирования Формы 5.1"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    queryset = Form51.objects.all()
    serializer_class = Form51CreateSerializer


class Form51DetailAPIView(RetrieveDestroyAPIView):
    """Удаления и  детейл Формы 5.1"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    queryset = Form51.objects.all()
    serializer = Form51ReserveSerializer


#
#
#
# class Form51DeleteAPIView(DestroyAPIView):
#     """Удаления Формы 5.1"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
#     queryset = Form51.objects.all()
#
#
# class ReserveDetailAPIView(APIView, ListWithPKMixin):
#     """ Резерв """
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     model = Form51
#     serializer = Form51ReserveSerializer
#     field_for_filter = "pk"


# class ReserveDelete(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
#
#     def delete(self, request, form_pk, reserve_pk):
#         form51 = get_object_or_404(Form51, pk=form_pk)
#         obj = get_object_or_404(Object, pk=reserve_pk)
#         if form51.reserve_object.filter(pk=reserve_pk).exists():
#             form51.reserve_object.remove(obj)
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderPhotoCreateView(APIView, PhotoCreateMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    model = Form51
    model_photo = OrderPhoto
    search_field_for_img = "order"


class OrderPhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    model = Form51
    model_for_delete = OrderPhoto


class SchemaPhotoCreateView(APIView, PhotoCreateMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    model = Form51
    model_photo = SchemaPhoto
    search_field_for_img = "schema"


class SchemaPhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser)
    model = Form51
    model_for_delete = SchemaPhoto


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