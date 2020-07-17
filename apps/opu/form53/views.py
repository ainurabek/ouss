from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, UpdateView
from apps.opu.form53.forms import Form53Form
from apps.opu.form53.models import Form53, Order53Photo, Schema53Photo
from rest_framework.views import APIView
from apps.opu.circuits.models import Circuit
from rest_framework.response import Response
from rest_framework import status
from apps.opu.form53.serializers import Form53CreateSerializer, Form53Serializer, Order53PhotoSerializer, Schema53PhotoSerializer
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView

from apps.opu.form51.models import Region

from apps.opu.form53.serializers import Region53Serializer

from apps.accounts.permissions import IsOpuOnly





class Form53CreateView(View):
    """ Создания Формы 5.3"""
    def post(self, request, pk):
        circuit = Circuit.objects.get(pk=pk)
        form = Form53Form(request.POST or None)
        if form.is_valid():
            form=form.save(commit=False)
            form.circuit = circuit
            form.save()
            for i in circuit.transit.all():
                if circuit != i:
                    Form53.objects.create(
                        circuit=i, order=form.order, schema=form.schema
                    )
            for i in circuit.transit2.all():
                if circuit != i:
                    Form53.objects.create(
                        circuit=i, order=form.order, schema=form.schema
                    )
            return redirect('apps:opu:form53:form53_list')
    def get(self, request, pk):
        form = Form53Form()
        return render(request, 'management/form53_create.html', {'form': form})


class Form53ListView(ListView):
    """ Список Формы 5.3 """
    model = Form53
    template_name = "management/form53_list.html"
    context_object_name = "form53_list"


class Form53UpdateView(UpdateView):
    """ Редактирования Формы 5.3 """
    model = Form53
    form_class = Form53Form
    success_url = reverse_lazy("apps:opu:form53:form53_list")
    template_name = "management/form53_create.html"


def form53_delete(request, pk):
    """ Удаления Форма 5.3 """
    if pk:
        Form53.objects.get(pk=pk).delete()

    return redirect("apps:opu:form53:form53_list")

class Region53ListView(ListView):
    """Список регионов"""
    model = Region
    template_name = "management/region53_list.html"
    context_object_name = "regions"


class FilterForm53View(View):
    """ Фильтрация Формы 5.3 по регионам """

    def get(self, request, slug):
        region = Region.objects.get(slug=slug)
        form53_list = Form53.objects.filter(circuit__id_object__id_outfit__outfit=region.name)
        return render(request,"management/form53_list.html", {"form53_list": form53_list})

# API
#############################################################################################


class Form53CreateViewAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    """Создания Формы 5.3"""
    def post(self, request, pk):
        circuit = Circuit.objects.get(pk=pk)
        if Form53.objects.filter(circuit=circuit).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = Form53CreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save(circuit=circuit, created_by=self.request.user.profile)

            for img in request.FILES.getlist('schema'):
                Schema53Photo.objects.create(src=img, form53=data)

            for img in request.FILES.getlist('order'):
                Order53Photo.objects.create(src=img, form53=data)
            for i in circuit.transit.all():
                if circuit != i:
                    Form53.objects.create(
                        circuit=i,
                        order=data.order, schema=data.schema, comments= data.comments
                    )
            for i in circuit.transit2.all():
                if circuit != i:
                    Form53.objects.create(
                        circuit=i,
                        order=data.order, schema=data.schema, comments= data.comments
                    )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Form53ListAPIView(ListAPIView):
    """Список Формы 5.3"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Form53Serializer

    def get_queryset(self):
        queryset = Form53.objects.all()
        region = self.request.query_params.get('region', None)
        customer = self.request.query_params.get('customer', None)
        category = self.request.query_params.get('category', None)
        circuit = self.request.query_params.get('circuit', None)

        if region is not None and region != "":
            queryset = queryset.filter(circuit__id_object__id_outfit__outfit=region)
        if customer is not None and customer != "":
            queryset = queryset.filter(circuit__customer=customer)
        if category is not None and category != "":
            queryset = queryset.filter(circuit__category=category)
        if circuit is not None and circuit != "":
            queryset = queryset.filter(circuit__name=circuit)
        return queryset



class Form53UpdateAPIView(UpdateAPIView):
    """Редактирования Формы 5.3"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    queryset = Form53.objects.all()
    serializer_class = Form53CreateSerializer


class Form53DeleteAPIView(DestroyAPIView):
    """Удаления Формы 5.3"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    queryset = Form53

class Region53ListAPIView(ListAPIView):
    """Список Регоинов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Region.objects.all()
    serializer_class = Region53Serializer


class Order53PhotoCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    def post(self, request, pk):
        form53 = Form53.objects.get(pk=pk)
        for img in request.FILES.getlist('order'):
            Order53Photo.objects.create(src=img, form53=form53)
        return Response(status=status.HTTP_201_CREATED)




class Order53PhotoDeleteView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def delete(self, request, form_pk, order_pk):
        form53=Form53.objects.get(pk=form_pk)
        order = Order53Photo.objects.get(pk=order_pk, form53=form53)
        print(order)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Schema53PhotoCreateView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    def post(self, request, pk):
        form53 = Form53.objects.get(pk=pk)
        for img in request.FILES.getlist('schema'):
            Schema53Photo.objects.create(src=img, form53=form53)
        return Response(status=status.HTTP_201_CREATED)


class Schema53PhotoDeleteView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def delete(self, request, form_pk, schema_pk):
        form53=Form53.objects.get(pk=form_pk)
        schema = Schema53Photo.objects.get(pk=schema_pk, form53=form53)
        schema.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
