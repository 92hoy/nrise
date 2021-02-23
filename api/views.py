from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import User, Session
from .serializers import *
from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponse, JsonResponse, Http404
from nrise.settings import SECRET_KEY, ALGORITHM
import json
import requests
import jwt
import bcrypt
from ipware.ip import get_client_ip

# Create your views here.
now = timezone.localtime()


class UserView(APIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="유저 생성",
        operation_description="post : /api/v1/user",
        request_body =CreateSerializer
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

            r_data = User.objects.filter(user_id=data['user_id'], del_yn='N').values('user_id', 'created_date')

            result = []
            result.append('회원가입 성공')
            result.append(r_data)
            return Response(result, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="유저 조회",
        operation_description="GET : /api/v1/user",
    )
    def get(self, request):
        data = request.data['id']
        user_info = User.objects.all().filter(id=data).values('id', 'user_id', 'created_date')

        session_info = Session.objects.all().filter(user_id=user_info[0]['user_id']).values('session_key', 'login_yn',
                                                                                            'logout_date',
                                                                                            'created_date').order_by(
            '-created_date')
        # 탈퇴여부 & 탈퇴했다면 탈퇴날짜 추가
        result = []
        result.append(user_info)
        result.append(session_info)
        return Response(result, status=200)
        # return JsonResponse({'user_info':json.dumps(list(user_info)),"session_info":json.dumps(list(session_info))}, status=200)

    @swagger_auto_schema(
        operation_summary="유저 탈퇴",
        operation_description="delete : /api/v1/user",
        request_body=DeleteSerializer,
    )
    def delete(self, request):
        session_key = request.data['session_key']
        try:
            # user_id catch
            if Session.objects.filter(session_key=session_key).latest('user_id'):
                user = Session.objects.filter(session_key=session_key).latest('user_id')

                queryset = User.objects.all().filter(user_id=user.user_id, del_yn='N')
                if len(queryset) == 0:
                    return Response('이미 탈퇴처리가 된 유저입니다.', status=202)

                queryset.update(del_yn='Y', modify_date=now)
            return Response('회원탈퇴 성공', status=200)
        except Exception as e:
            return Response('없는 session값 입니다.', status=500)


class SignView(APIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="로그인",
        operation_description="put : /api/v1/sign",
        request_body=LoginSerializer,

    )
    def put(self, request, format=None):
        data = request.data

        try:
            if User.objects.filter(user_id=data['user_id']).filter(del_yn='N').exists():
                account = User.objects.get(user_id=data['user_id'])
                # print('-----check')
                if bcrypt.checkpw(data['password'].encode('utf-8'), account.password.encode('utf-8')):
                    token = jwt.encode({'user_id': account.id}, SECRET_KEY, algorithm=ALGORITHM)

                    if not request.session.session_key:
                        # print('save')
                        request.session.save()

                    # request.session['test'] = 'Test'
                    # print('request.session', request.session.session_key)
                    # print('request.session[test]', request.session['test'])
                    # print(type(request.session.session_key))
                    session_id = str(request.session.session_key)
                    # 세션 만료 체크
                    if Session.objects.filter(user_id=data['user_id']).order_by(
                            'created_date').last().session_key != str(request.session.session_key):
                        print('세션 만료되어 새로 로그인합니다.')

                    ip, tmp = get_client_ip(request)
                    print('세션 갱신')
                    queryset = User.objects.all().filter(user_id=data['user_id'], del_yn='N')
                    queryset.update(last_login=now, modify_date=now)
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

                return Response('탈퇴 회원입니다.', status=400)
            else:
                return Response('없는 회원입니다.', status=400)

        except KeyError as e:
            return Response(e, status=500)

    @swagger_auto_schema(
        operation_summary="로그아웃",
        operation_description="delete : /api/v1/sign",
        request_body=LogoutSerializer,
    )

    def delete(self, request):
        session_key = request.data['session_key']
        # serializer_class = LogoutSerializer
        try:
            # user_id catch
            if Session.objects.filter(session_key=session_key).latest('user_id'):
                user = Session.objects.filter(session_key=session_key).latest('user_id')
                ip, tmp = get_client_ip(request)

                '''
                이미 로그아웃 된경우를 catch 하려면 활성화 
                '''
                # if user.login_yn == 'N':
                #     Session(
                #         user_id=user.user_id,
                #         session_key=session_key,
                #         ip_address=ip,
                #         login_yn='N',
                #         logout_date=now
                #     ).save()
                #     return Response('이미 로그아웃 상태입니다.', status=202)

                # louout session insert
                Session(
                    user_id=user.user_id,
                    session_key=session_key,
                    ip_address=ip,
                    login_yn='N',
                    logout_date=now
                ).save()
                # user logout_date set
                queryset = User.objects.all().filter(user_id=user.user_id, del_yn='N')
                queryset.update(last_logout=now, modify_date=now)

                return Response('Logout Success', status=200)

            else:
                return Response('올바른 세션값이 아닙니다.', status=401)

        except Exception as e:
            print('delete_error', e)
            return Response('올바른 세션값이 아닙니다.', status=500)
