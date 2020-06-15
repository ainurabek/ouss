from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView, UpdateView
from apps.opu.form53.forms import Form53Form
from apps.opu.form53.models import Form53
from rest_framework.views import APIView
from apps.opu.circuits.models import Circuit
from rest_framework.response import Response
from rest_framework import status
from apps.opu.form53.serializers import Form53CreateSerializer, Form53Serializer
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView

from apps.dispatching.models import Region

from apps.opu.form53.serializers import Region53Serializer

from apps.opu.customer.models import Customer

from apps.opu.form_customer.models import Form_Customer


class CustomerListView(ListView):
    """Список арендаторов"""
    model = Customer
    template_name = "management/customer_list.html"
    context_object_name = "customers"

class FilterFormCustView(View):
    """ Фильтрация Формы арендаторов  по арендаторам """

    def get(self, request, pk):
        customer = Customer.objects.get(id=pk)
        form_cust = Form_Customer.objects.filter(customer=customer)
        return render(request,"management/form_customer_list.html", {"form_cust": form_cust})

class FormCustListView(ListView):
    """ Список Формы 5.3 """
    model = Form_Customer
    template_name = "management/form_customer_list.html"
    context_object_name = "form_customer_list"