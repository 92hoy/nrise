# restful-api


## Development Environment
```
macOS
python 3.7.9
mysql 8.0.23 for osx10.16 on x86_64 (Homebrew)
```

## Configuring a project

```bash
$ git clone https://github.com/92hoy/nrise
$ cd nrise
```

## Getting Started with Project

#### set
```bash
$ cd nrise
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver 127.0.0.1:8000
```

#### DB
```
--(in settings.py)
host = localhost
port = 3306
DATABASE = nrise
PASSWORD = 0000
```


## 회원가입
-[POST]    /api/v1/user      
```
[form-data]
user_id
password
```
## 회원조회
-[GET] /api/v1/user   
```
[form-data]
id (회원고유값 PK)
```
## 회원탈퇴
-[DELETE]    /api/v1/user     
```
[form-data]
session_key(세션 고유값)
```
## 로그인
-[PUT] /api/v1/sign     
```
[form-data]
user_id
password
```
## 로그아웃
-[DELETE]  /api/v1/sign      
```
[form-data]
session_key(세션 고유값)

```
