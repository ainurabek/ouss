from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from knox.auth import TokenAuthentication
from apps.opu.customer.models import Customer
from apps.opu.customer.serializers import CustomerSerializer
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.accounts.permissions import IsOpuOnly
from rest_framework.views import APIView

from apps.opu.customer.service import get_customer_diff


class CustomerViewSet(viewsets.ModelViewSet):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	lookup_field = 'pk'
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	filter_backends = (SearchFilter, DjangoFilterBackend)
	search_fields = ('customer', 'abr', 'adding', 'contact_name')
	filterset_fields =  ('customer', 'abr', 'adding', 'contact_name')


class CustomerEditView(generics.RetrieveUpdateAPIView):
	lookup_field = 'pk'
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated, IsOpuOnly,)

	def perform_update(self, serializer):
		serializer.save(created_by=self.request.user.profile)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated, IsOpuOnly,))
def customer_delete_view(request, pk):
	try:
		customer = Customer.objects.get(id=pk)
	except customer.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == "DELETE":
		operation = customer.delete()
		data = {}
		if operation:
			data["success"] = "Арендатор успешно удален"
		else:
			data["failure"] = "Арендатор успешно удален"
		return Response(data=data)

class CustomerHistory(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

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

