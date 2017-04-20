# tdt4140G70-backend

## Project setup:

1. Install python3 in your path

2. Clone and start the django app:

* Linux:
```
git clone git@github.com:orhanhenrik/tdt4140G70-backend.git
cd tdt4140G70-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
* Windows:
```
git clone https://github.com/orhanhenrik/tdt4140G70-backend.git
cd tdt4140G70-backend
py -3 -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

deactivate
```

## Checking coverage:
```
coverage run --source='.' --omit='venv/*,*/wsgi.py,*/apps.py,*/migrations/*,manage.py'  manage.py test
coverage report
```