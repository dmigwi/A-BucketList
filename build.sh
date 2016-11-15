python manage.py db init
python manage.py db migrate
python manage.py db upgrade
gunicorn manage:app 