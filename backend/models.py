from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='idx')
    user_id = models.CharField(null=False, max_length=255, verbose_name='Login_id')
    password = models.CharField(null=False, max_length=255, verbose_name='Login_password')
    username = models.CharField(null=False, max_length=50, verbose_name='사용자 이름')
    del_yn = models.CharField(null=False, max_length=2, verbose_name='삭제 여부', default='N')
    last_login = models.DateTimeField(verbose_name='마지막 로그인 시간')
    last_logout = models.DateTimeField(verbose_name='마지막 로그아웃 시간')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성 날짜')
    modify_date = models.DateTimeField(auto_now=True, verbose_name='수정 날짜')

    class Meta:
        # abstract = True
        managed = True
        db_table = 'user'
        app_label = 'user'
        ordering = ['id', ]
        verbose_name_plural = 'User_Info'


class Session(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='idx')
    user_id = models.CharField(null=False, max_length=255, verbose_name='Login_id')
    session_key = models.CharField(null=False, max_length=255, verbose_name='session_key')
    ip_address = models.CharField(null=False, max_length=20, verbose_name='IP주소')
    login_yn = models.CharField(null=False, max_length=2, verbose_name='로그인 여부')
    detail_info = models.CharField(null=False, max_length=255, verbose_name='세부사항')
    logout_date = models.DateTimeField(verbose_name='로그아웃 시간')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='생성 날짜')

    class Meta:
        # abstract = True
        managed = True
        db_table = 'session'
        app_label = 'session'
        ordering = ['id', ]
        verbose_name_plural = 'session_History'
