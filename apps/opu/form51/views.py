from django.shortcuts import redirect, render
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from django.urls import reverse_lazy
from django.views.generic import View, ListView, UpdateView


from apps.opu.form51.forms import Form51Form
from apps.opu.form51.models import Form51, Region
from apps.opu.form51.serializers import Form51CreateSerializer, Form51Serializer, RegionSerializer, \
    Form51ReserveSerializer
from apps.opu.objects.models import Object
from rest_framework.parsers import MultiPartParser, FormParser


# Templates


class Form51CreateView(View):
    """ Создания Формы 5.1"""

    def post(self, request, pk):
        obj = Object.objects.get(pk=pk)
        form = Form51Form(request.POST or None)
        if form.is_valid():
            form=form.save(commit=False)
            form.object = obj
            form.save()

            for i in obj.transit.all():
                if obj != i:
                    Form51.objects.create(
                        object=i, customer=form.customer,
                        num_ouss=form.num_ouss,
                        order=form.order, schema=form.schema,
                        reserve=form.reserve
                    ) #index_ko=form.index_ko,

            for i in obj.transit2.all():
                if obj != i:
                    Form51.objects.create(
                        object=i, customer=form.customer,
                         num_ouss=form.num_ouss,
                        order=form.order, schema=form.schema,
                        reserve=form.reserve
                    ) #index_ko=form.index_ko,

            return redirect('apps:opu:form51:form_list')


    def get(self, request, pk):

        form = Form51Form()
        return render(request, 'management/form51_create.html', {'form': form})


class Form51ListView(ListView):
    """ Список Формы 5.1 """
    model = Form51
    template_name = "management/form51_list.html"
    context_object_name = "form51_list"


class Form51UpdateView(UpdateView):
    """ Редактирования Формы 5.1 """
    model = Form51
    form_class = Form51Form
    success_url = reverse_lazy("apps:opu:form51:form_list")
    template_name = "management/form51_create.html"


def form51_delete(request, pk):
    """ Удаления Форма 5.1 """
    if pk:
        Form51.objects.get(pk=pk).delete()

    return redirect("apps:opu:form51:form_list")


class RegionListView(ListView):
    """Список регионов"""
    model = Region
    template_name = "management/region_list.html"
    context_object_name = "regions"


class FilterForm51View(View):
    """ Фильтрация Формы 5.1 по регионам """

    def get(self, request, slug):
        region = Region.objects.get(slug=slug)
        form51_list = Form51.objects.filter(object__id_outfit__outfit=region.name)
        return render(request,"management/form51_list.html", {"form51_list": form51_list})


class ReserveDetailView(View):
    """ Информация о резерве """

    def get(self, request, pk):
        obj = Form51.objects.get(pk=pk)
        return render(request, "management/reserve_detail.html", {"form51_reserve": obj})


# API
#############################################################################################



class FormCreateViewAPI(APIView):
    """Создания Формы 5.1"""

    def post(self, request, pk):
        obj = Object.objects.get(pk=pk)
        serializer = Form51CreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save(object=obj, created_by=self.request.user.profile)

            for i in obj.transit.all():
                if obj != i:
                    Form51.objects.create(
                        object=i, customer=data.customer,
                        num_ouss=data.num_ouss,
                        order=data.order, schema=data.schema,
                        reserve=data.reserve
                    )

            for i in obj.transit2.all():
                if obj != i:
                    Form51.objects.create(
                        object=i, customer=data.customer,
                        num_ouss=data.num_ouss,
                        order=data.order, schema=data.schema,
                        reserve=data.reserve
                    )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormListAPIView(ListAPIView):
    """Список Формы 5.1"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Form51Serializer

    def get_queryset(self):
        queryset = Form51.objects.all()
        region = self.request.query_params.get('region', None)
        customer = self.request.query_params.get('customer', None)

        if region is not None and region != "":
            queryset = queryset.filter(object__id_outfit__outfit=region)
        if customer is not None and customer != "":
            queryset = queryset.filter(customer__customer=customer)

        return queryset


class Form51UpdateAPIView(UpdateAPIView):
    """Редактирования Формы 5.1"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Form51.objects.all()
    serializer_class = Form51CreateSerializer


class Form51DeleteAPIView(DestroyAPIView):
    """Удаления Формы 5.1"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Form51.objects.all()


class RegionListAPIView(ListAPIView):
    """Список Регоинов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class ReserveDetailAPIView(APIView):
    """ Резерв """

    def get(self, request, pk):
        form51 = Form51.objects.get(pk=pk)
        serializer = Form51ReserveSerializer(form51)
        return Response(serializer.data)

class ReserveDelete(APIView):
    def delete(self, request, form_pk, reserve_pk):
        form51=Form51.objects.get(pk=form_pk)
        obj=Object.objects.get(pk=reserve_pk)
        if form51.reserve_object.filter(pk=reserve_pk).exists():
            form51.reserve_object.remove(obj)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)






