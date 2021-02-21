from backend.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        user = User.objects.all()
        model = User
        fields = '__all__'
        # fields = ('id', 'created_at', 'title', 'category', 'star_rating',)  # req, res 시 사용되길 원하는 필드(컬럼)만 적어줘도 됨.
