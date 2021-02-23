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
