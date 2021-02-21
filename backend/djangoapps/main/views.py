from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from django.views import View
from django.http import Http404

from backend.models import User
from backend.serializers import UserSerializer


# Create your views here.

class UserViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   View):
    serializer_class = UserSerializer

    def get_queryset(self):

        user_info = User.objects.all()
        if not user_info.exists():
            raise Http404()

        return user_info

    def add(self, request):
        users = User.objects.filter(**request.data)
        if users.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        user_serializer = UserSerializer(data=request.data, partial=True)
        if not user_serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        user = user_serializer.save()

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)