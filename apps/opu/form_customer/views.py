from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, ListView
from rest_framework.views import APIView
from apps.opu.circuits.models import Circuit
from rest_framework.response import Response
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView, DestroyAPIView, ListAPIView
from apps.opu.customer.models import Customer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.opu.form_customer.models import Form_Customer, OrderCusPhoto
from apps.opu.form_customer.forms import FormCustForm
from apps.opu.form_customer.serializers import FormCustomerCreateSerializer, FormCustomerSerializer, \
    CircuitListSerializer
from apps.opu.form_customer.serializers import CustomerFormSerializer
from apps.opu.form_customer.serializers import ObjectFormCustomer
from apps.opu.objects.models import Object
from apps.accounts.permissions import IsOpuOnly
from apps.opu.services import PhotoDeleteMixin, PhotoCreateMixin, ListWithPKMixin, create_photo


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



#API
#######################################################################################################################
class CustomerFormListView(ListAPIView):
    """Список арендаторов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerFormSerializer
    queryset = Customer.objects.all()


class FormCustomerListAPIView(ListAPIView):
    """ Фильтрация Формы арендаторов  по арендаторам """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('object', 'circuit', 'customer')
    queryset = Form_Customer.objects.all()
    serializer_class = FormCustomerSerializer


class CircuitListAPIView(APIView, ListWithPKMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Circuit
    serializer = CircuitListSerializer
    field_for_filter = "customer_id"


class ObjectListAPIView(APIView, ListWithPKMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Object
    serializer = ObjectFormCustomer
    field_for_filter = "customer_id"


class FormCustomerCircCreateAPIView(APIView):
    """Создания Формы арендаторов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def post(self, request, pk):
        circuit = get_object_or_404(Circuit, pk=pk)
        if Form_Customer.objects.filter(circuit=circuit).exists():
            content = {'По такому каналу уже форма арендаторов создана'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        serializer = FormCustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save(circuit=circuit, customer=circuit.customer, created_by=self.request.user.profile)
            create_photo(model=Form_Customer, model_photo=OrderCusPhoto, obj=data, field_name="order", request=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormCustomerObjCreateAPIView(APIView):
    """Создания Формы арендаторов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    def post(self, request, pk):
        object = get_object_or_404(Object, pk=pk)
        if Form_Customer.objects.filter(object=object).exists():
            content = {'По такому обьекту уже форма арендаторов создана'}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        serializer = FormCustomerCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save(object=object, customer=object.customer, created_by=self.request.user.profile)
            create_photo(model=Form_Customer, model_photo=OrderCusPhoto, obj=data, field_name="order", request=request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FormCustomerUpdateAPIView(UpdateAPIView):
    """Создания Формы арендаторов"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    queryset = Form_Customer.objects.all()
    serializer_class = FormCustomerCreateSerializer


class FormCustomerDeleteAPIView(DestroyAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    queryset = Form_Customer.objects.all()


class OrderCusPhotoCreateView(APIView, PhotoCreateMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)

    model = Form_Customer
    model_photo = OrderCusPhoto
    search_field_for_img = "order"

    def post(self, request, pk):
        form_cus = Form_Customer.objects.get(pk=pk)
        for img in request.FILES.getlist('order'):
            OrderCusPhoto.objects.create(order=img, form_customer=form_cus)
        return Response(status=status.HTTP_201_CREATED)



class OrderCusPhotoDeleteView(APIView, PhotoDeleteMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOpuOnly,)
    model_for_delete = OrderCusPhoto
