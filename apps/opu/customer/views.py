from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from knox.auth import TokenAuthentication
from apps.opu.customer.models import Customer
from apps.opu.customer.serializers import CustomerSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permissions import IsPervichkaOnly, SuperUser, IngenerUser
from rest_framework.views import APIView

from apps.opu.customer.service import get_customer_diff

from apps.logging.customer.views import CustomerLogUtil


class CustomerViewSet(viewsets.ModelViewSet):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	lookup_field = 'pk'
	authentication_classes = (TokenAuthentication,)
	filter_backends = (SearchFilter, DjangoFilterBackend)
	search_fields = ('customer', 'abr', 'adding', 'diapozon')
	filterset_fields =  ('customer', 'abr', 'adding', 'diapozon')

	def get_permissions(self):
		if self.action == 'list' or 'retrieve':
			permission_classes = [IsAuthenticated, ]
		else:
			permission_classes = [IsAuthenticated, IsPervichkaOnly | SuperUser, SuperUser | IngenerUser]
		return [permission() for permission in permission_classes]

	def perform_create(self, serializer):
		instance = serializer.save()
		CustomerLogUtil(self.request.user, instance.pk).obj_create_action('customer_created')


class CustomerHistory(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated, IsPervichkaOnly, )

	def get(self, request, pk):
		customer = Customer.objects.get(pk=pk)
		histories = customer.history.all()
		data = []
		for h in histories:
			a = {}
			a['history_id'] = h.history_id
			a['updated_date'] = h.history_date
			a['updated_by'] = h.history_user.username
			a['change_method'] = h.get_history_type_display()
			a['changes'] = get_customer_diff(history=h)
			if a['changes'] == "" and h.history_type =='~':
				continue
			data.append(a)
		return Response(data, status=status.HTTP_200_OK)
