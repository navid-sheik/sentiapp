release: python manage.py migrate
web: daphne sentiapp.asgi:application --port $PORT --bind 0.0.0.0 -v2
# celery: celery -A sentiapp.celery worker -l info 
celery : celery -A sentiapp worker -l info --concurrency 2
celerybeat: celery -A sentiapp beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
celeryworker: celery -A sentiapp.celery worker  & celery -A sentiapp beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler & wait -n