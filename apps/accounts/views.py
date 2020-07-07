import datetime

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.db.models import Q
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework import permissions, viewsets, status, generics
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from .serializers import LoginUserSerializer, UserSerializer, ProfileListSerializer, CreateUserSerializer, \
    DepartmentSerializer, SubdepartmentSerializer, LogSerializer
from django.http.response import HttpResponse, JsonResponse
from .models import Profile, DepartmentKT, SubdepartmentKT, Log
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

User = get_user_model()

class Register(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', False)
        print(username)
        password = request.data.get('password', False)
        role = request.data.get('role', False)
        print(role)
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
        try:
            profile = Profile.objects.get(user__username=user)
            profile.online = True
            profile.save()
            if Log.objects.filter(Q(user=profile) & Q(date__gt=timezone.now())).exists():
                pass
            else:
                end_date = timezone.now()+datetime.timedelta(days=1)
                Log.objects.create(user=profile, start_at=timezone.now(), date=end_date)
        except ObjectDoesNotExist:
            pass

        login(request, user)
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        profile = Profile.objects.get(user__username=request.user.username)
        profile.online = False
        profile.save()
        if Log.objects.filter(Q(user=request.user.profile) & Q(date__gt=timezone.now())).exists():
            Log.objects.filter(Q(user=request.user.profile) & Q(date__gt=timezone.now())).update(end_time=timezone.now())
        return HttpResponse("Пользователь вышел из системы", None, status=status.HTTP_204_NO_CONTENT)

'''
Данная функция позволяет создать профиль сотрудника. Из фронта приходят данные, которые вводит юзер, также его id (role, user and password)
'''
class CreateProfileAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def post(self, request):
        data = request.data
        user = request.user
        print(user)
        first_name = data['first_name']
        last_name = data['last_name']
        middle_name = data['middle_name']
        position = data['position']
        gender = data['gender']
        phone_number = data['phone_number']
        profile = Profile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                         middle_name=middle_name, position=position, gender=gender,
                                         phone_number=phone_number, online=True)
        return HttpResponse(profile, status=status.HTTP_201_CREATED)


class ProfileListAPIView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Profile.objects.all()
    lookup_field = 'pk'
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
    print(department.id)
    user = request.user
    print(user)
    if user.department.id != department.id:
        print(user.department.id)
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
    print(department.id)
    print(subdepartment.id)
    user = request.user
    print(user)
    if user.department.id != department.id and user.subdeparment.id != subdepartment.id:
        print(user.department.id)
        print(user.subdepartment.id)
        return JsonResponse({'error': 'Вы не имеете право зайти в этот отдел'}, status=401)
    else:
        return JsonResponse({'success': 'Success'}, status=202)


class LogListAPIView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LogSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('user', 'start_at', 'end_time')

    def get_queryset(self):
        subdep = SubdepartmentKT.objects.get(id=2)
        queryset = Log.objects.filter(user__subdepartment=subdep)
        return queryset

















