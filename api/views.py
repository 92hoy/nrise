from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import User,Session
from .serializers import UserSerializer, UserSerializer_check
from django.db.models import Count
from django.http import HttpResponse, JsonResponse, Http404
from nrise.settings import SECRET_KEY, ALGORITHM
import json
import requests
import jwt
import bcrypt
from ipware.ip import get_client_ip


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
        else:
            User(
                user_id=data['user_id'],
                password=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode()
            ).save()
            # user_serializer = UserSerializer(data=request.data, partial=True)
            r_data = User.objects.filter(user_id=data['user_id'], del_yn='N').values('user_id','created_date')
            return Response(r_data, status=status.HTTP_201_CREATED)

        # password = data['password'].encode('utf-8')
        # request.data['password'] = bcrypt.hashpw(password, bcrypt.gensalt()).decode()
        # user_serializer = UserSerializer(data=request.data, partial=True)
        # if not user_serializer.is_valid():
        #     return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        #
        # # user = user_serializer.save()
        #
        # return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

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


class SignView(APIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="로그인",
        operation_description="put : /api/v1/session",
    )
    def put(self, request, format=None):
        data = request.data

        try:
            if User.objects.filter(user_id=data['user_id']).filter(del_yn='N').exists():
                account = User.objects.get(user_id=data['user_id'])
                print('-----check')
                if bcrypt.checkpw(data['password'].encode('utf-8'), account.password.encode('utf-8')):
                    token = jwt.encode({'user_id': account.id}, SECRET_KEY, algorithm=ALGORITHM)


                    if not request.session.session_key:
                        print('save')
                        request.session.save()

                    request.session['test'] = 'Test'
                    print('request.session', request.session.session_key)
                    print('request.session[test]',request.session['test'])
                    print(type(request.session.session_key))
                    session_id = str(request.session.session_key)
                    print('get_client_ip(request)',type(get_client_ip(request)))
                    ip,tmp  =get_client_ip(request)
                    Session(
                        user_id=data['user_id'],
                        session_key=session_id,
                        ip_address=ip,
                        login_yn='Y'
                    ).save()

                    # session insert --------here

                    return Response('Login Success', status=200)

                return Response('password 가 맞지 않습니다.', status=401)

            elif User.objects.filter(user_id=data['user_id']).filter(del_yn='Y').exists():

                return Response('탈퇴된 회원입니다.', status=400)
            else:
                return Response('없는 회원입니다.', status=400)

        except KeyError as e:
            return Response(e, status=500)
