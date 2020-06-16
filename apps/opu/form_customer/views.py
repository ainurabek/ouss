from django.shortcuts import redirect, render, get_object_or_404
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

from apps.opu.form_customer.forms import FormCustForm


class CustomerListView(ListView):
    """Список арендаторов"""
    model = Customer
    template_name = "management/customer_list.html"
    context_object_name = "customers"


class MenuCustView(View):
    """ Фильтрация Формы арендаторов  по арендаторам """

    def get(self, request, pk):
        customer = Customer.objects.get(id=pk)
        return render(request,"management/form_cust_menu.html", {"customer": customer})

class FilterFormCustView(View):
    """ Фильтрация Формы арендаторов  по арендаторам """

    def get(self, request, pk):
        customer = Customer.objects.get(id=pk)
        form_cust = Form_Customer.objects.filter(customer=customer)
        return render(request,"management/form_customer_list.html", {"form_cust": form_cust, "customer": customer})

class FilterCircuitView(View):
    """ Фильтрация Формы арендаторов  по арендаторам """

    def get(self, request, pk):
        customer = Customer.objects.get(id=pk)
        circuits = Circuit.objects.filter(customer=customer)
        return render(request,"management/form_customer_circuits.html", {"circuits": circuits, "customer":customer})


class FormCustCircCreateView(View):

    def post(self, request, pk):
        circuit = Circuit.objects.get(pk=pk)
        form = FormCustForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.circuit = circuit
            form.customer = circuit.customer
            form.save()
            return redirect('apps:opu:form_customer:filter_form_cust', form.customer.id)

    def get(self, request, pk):
        form = FormCustForm()
        return render(request, 'management/form_cust_create.html', {'form': form})


def form_cust_edit(request, pk):
    form_customer = get_object_or_404(Form_Customer, id=pk)
    print(form_customer)
    if request.method == "POST":
        form = FormCustForm(request.POST, instance=form_customer)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            return redirect('apps:opu:form_customer:filter_form_cust', form_customer.customer.id)
    else:
        form=FormCustForm(instance=form_customer)
    return render(request, 'management/form_cust_create.html', {'form': form})

def form_cust_delete(request, pk):
    customer_id=Form_Customer.objects.get(pk=pk).customer.id
    if pk:
        Form_Customer.objects.get(pk=pk).delete()
    return redirect("apps:opu:form_customer:filter_form_cust", customer_id)
