import datetime

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, login, logout
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, viewsets, status
from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.auth import TokenAuthentication

from .permissions import IsCreator, SuperUser
from .serializers import LoginUserSerializer, UserSerializer, ProfileListSerializer, CreateUserSerializer, \
    DepartmentSerializer, SubdepartmentSerializer, LogSerializer, LogUpdateSerializer, ChangePasswordSerializer
from django.http.response import HttpResponse, JsonResponse
from .models import Profile, DepartmentKT, SubdepartmentKT, Log
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import permission_classes
from rest_framework.generics import  get_object_or_404


User = get_user_model()

class Register(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', False)
        password = request.data.get('password', False)
        role = request.data.get('role', False)
        department = request.data.get('department', False)
        subdepartment = request.data.get('subdepartment', False)

        if username and password and role and department and subdepartment:
            user = User.objects.filter(username=username)
            if user.exists():
                return Response({'status': False,
                                 'detail': 'Email already have account associated. Kindly try forgot password'})
            else:

                Temp_data = {'username': username, 'password': password, 'role': role, 'department':department,
                             'subdeparment':subdepartment}
                serializer = CreateUserSerializer(data=Temp_data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                user.set_password(user.password)
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse('Username не указан', safe=False)


'''
Данная функция позволяет залогиниться зарегистрированному ползователю. Необходимо, чтобы фрон отправил логин и пароль юзера
'''

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        # username = User.objects.get(username=request.data["username"])
        # Profile.objects.filter(user=username).update(start_at=datetime.datetime.now())

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']


        login(request, user)
        if request.user.is_profile_created:
            profile = Profile.objects.get(user__username=user)
            profile.online = True
            profile.save()
        return super().post(request, format=None)


'''
Данная функция показывает всех существующих юзеров
'''


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LogoutView(APIView):
    def get(self, request, format=None):
        if request.user.role.id == 1:
            pass
        else:
            if request.user.is_profile_created:
                profile = Profile.objects.get(user__username=request.user.username)
                profile.online = False
                profile.save()
        logout(request)
        return Response(status=status.HTTP_200_OK)


'''
Данная функция позволяет создать профиль сотрудника. Из фронта приходят данные, которые вводит юзер, также его id (role, user and password)
'''


class CreateProfileAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def post(self, request):
        data = request.data
        user = request.user

        first_name = data['first_name']
        last_name = data['last_name']
        middle_name = data['middle_name']
        position = data['position']
        gender = data['gender']
        phone_number = data['phone_number']
        profile = Profile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                         middle_name=middle_name, position=position, gender=gender,
                                         phone_number=phone_number, online=True)

        user.is_profile_created = True
        user.save()
        response = {"data": "Профиль пользователя успешно создан"}
        return HttpResponse(response, status=status.HTTP_201_CREATED)


class ProfileListAPIView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            queryset = Profile.objects.filter(user=user)
        except ObjectDoesNotExist:
            pass
        return queryset


class AllProfileAPIView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Profile.objects.all().order_by('last_name')
    serializer_class = ProfileListSerializer


'''
Данная функция позволяет создать отделы КТ
'''


class DepartmentKTAPIView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = DepartmentKT.objects.all()
    lookup_field = 'pk'
    serializer_class = DepartmentSerializer


def department_view(request, department_id):
    department = DepartmentKT.objects.get(id=department_id)
    user = request.user
    if user.department.id != department.id:
        return JsonResponse({'error': 'Вы не имеете право зайти в этот отдел'}, status=401)
    else:
        return JsonResponse({'success': 'Success'}, status=202)


'''
Данная функция позволяет создать подотделы КТ
'''


class SubdepartmentKTAPIView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = SubdepartmentKT.objects.all()
    lookup_field = 'pk'
    serializer_class = SubdepartmentSerializer


def subdepartment_view(request, department_id, subdepartment_id):
    department = DepartmentKT.objects.get(id=department_id)
    subdepartment= SubdepartmentKT.objects.get(department=department, id=subdepartment_id)
    user = request.user
    if user.department.id != department.id and user.subdeparment.id != subdepartment.id:
        return JsonResponse({'error': 'Вы не имеете право зайти в этот отдел'}, status=401)
    else:
        return JsonResponse({'success': 'Success'}, status=202)


class LogListAPIView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LogSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('user',)

    def get_queryset(self):
        queryset = Log.objects.all()
        start_at = self.request.query_params.get('start_at', "")
        end_time = self.request.query_params.get('end_time', "")

        if start_at != "":
            queryset = queryset.filter(start_at__date__gte=start_at)
        if end_time != "":
            queryset = queryset.filter(end_time__date=end_time)
        return queryset


class LogUpdateAPIView(UpdateAPIView):
    queryset = Log.objects.all()
    permission_classes = (IsAuthenticated, IsCreator,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = LogUpdateSerializer

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.end_time is not None and instance.end_time < datetime.datetime.now():
            return Response(status=status.HTTP_403_FORBIDDEN)


class LogCreateAPIView(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = LogUpdateSerializer
    queryset = Log.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)


class ChangePasswordView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, SuperUser)
    search_fields = ('name',)
    serializer = ChangePasswordSerializer

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.object = user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {"detail": "Пароль для {} успешно изменен".format(user)}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

