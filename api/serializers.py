from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        user = User.objects.all()
        model = User
        fields = '__all__'
        # fields = ('user_id', 'user_name', 'create_date')


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        # user = User.objects.all()
        model = User
        fields = ['user_id', 'password']


class DeleteSerializer(serializers.ModelSerializer):
    class Meta:
        # user = User.objects.all()
        model = Session
        fields = ['session_key']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        # user = User.objects.all()
        model = User
        fields = ['user_id', 'password']
    # user_id = serializers.CharField(help_text=''' 사용할 아이디''', required=True, allow_blank=True)
    # password = serializers.CharField(help_text=''' 비밀번호 ''', required=True, allow_blank=True)


class LogoutSerializer(serializers.ModelSerializer):
    class Meta:
        # user = User.objects.all()
        model = Session
        fields = ['session_key']
    # session_key = models.CharField(help_text=''' session_key ''')


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        session = Session.objects.all()
        model = session
        fields = '__all__'

# class UserSerializer_check(serializers.Serializer):
#     user_id = serializers.CharField(help_text=''' 사용할 아이디''', required=True, allow_blank=True)
#     password = serializers.CharField(help_text=''' 비밀번호 ''', required=True, allow_blank=True)
