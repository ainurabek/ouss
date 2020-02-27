from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from .models import Profile, DepartmentKT

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'role', 'department')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'role', 'department', 'password')


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            if User.objects.filter(username=username).exists():
                user = authenticate(request=self.context.get('request'),
                                    username=username, password=password)

            else:
                msg = {'message': 'Данный пользователь не зарегистрирован.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'message': 'Невозможно войти с предоставленными учетными данными. Обратитесь к админстратору', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Должны быть указаны "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentKT
        fields = '__all__'

class ProfileListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'user', 'position','first_name', 'last_name', 'middle_name', 'online',
                  'gender', 'phone_number')
        depth = 1










