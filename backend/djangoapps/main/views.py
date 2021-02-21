from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.views import View
from django.http import Http404
from backend.models import User
from backend.serializers import UserSerializer, UserSerializer_check
from django.db.models import Count
import json


# Create your views here.

class UserView(APIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="유저 생성",
        operation_description="GET : /api/v1/user",
    )
    def post(self, request, format=None):
        data = request.data
        check = User.objects.filter(del_yn='N', user_id=data['user_id']).annotate(Count('id'))
        if len(check) > 0:
            return Response("이미 사용중인 아이디입니다", status=500)

        user_serializer = UserSerializer(data=request.data, partial=True)
        if not user_serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        user = user_serializer.save()

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="유저 조회",
        operation_description="GET : /api/v1/user",
    )
    def get(self, request):
        data = request.data['id']
        print(data)
        # filter_dict = {
        #     'id': self.request.GET.get('id', None),
        #     'user_id__contains': self.request.GET.get('user_id', None),
        #     'username__contains': self.request.GET.get('username', None)
        # }

        # print('filter_dict', filter_dict)
        # filtering = {key: val for key, val in filter_dict.items() if val is not None}
        # print('filtering', filtering)

        user_info = User.objects.all().filter(id=data).values('id', 'user_id', 'created_date')
        print('user_info', user_info)
        # serializer = UserSerializer(data=request.data, partial=True)
        # if not user_info.exists():
        #     raise Http404()
        # 탈퇴여부 & 탈퇴했다면 탈퇴날짜 추가
        return Response(user_info, status=200)

    @swagger_auto_schema(
        operation_summary="유저 수정",
        operation_description="GET : /api/v1/user",
    )
    def put(self, request):
        print(
            'update'
        )
        return

    @swagger_auto_schema(
        operation_summary="유저 탈퇴",
        operation_description="GET : /api/v1/user",
    )
    def delete(self, request):
        print(
            'delete'
        )
        return
