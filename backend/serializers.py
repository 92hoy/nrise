from backend.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        user = User.objects.all()
        model = User
        fields = '__all__'
        # fields = ('user_id', 'user_name', 'create_date')


class UserSerializer_check(serializers.Serializer):
    user_id = serializers.CharField(help_text=''' 사용할 아이디''', required=True, allow_blank=True)
    username = serializers.CharField(help_text=''' 사용자 이름 ''', required=True, allow_blank=True)
    password = serializers.CharField(help_text=''' 비밀번호 ''', required=True, allow_blank=True)
