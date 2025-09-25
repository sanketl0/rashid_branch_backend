celery -A autocount.celery worker -l info

celery -A autocount.celery worker --loglevel=info -P eventlet