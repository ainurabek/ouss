from django.shortcuts import render
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from knox.auth import TokenAuthentication
from apps.opu.customer.models import Customer
from apps.opu.customer.serializers import CustomerSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly




class CustomerViewSet(viewsets.ModelViewSet):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	lookup_field = 'pk'
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticatedOrReadOnly,)
	filter_backends = (SearchFilter, DjangoFilterBackend)
	search_fields = ('customer', 'abr', 'adding', 'our_services_to', 'connection_points')
	filterset_fields =  ('customer', 'abr', 'adding', 'our_services_to', 'connection_points')