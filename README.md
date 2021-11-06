# flask_celery_redis

Simple flask application that implements background task worker using Celery and Redis

(execute from inside venv) to run this test application...

terminal 1: python app.py
terminal 2: ./run_redis.sh
terminal 3: celery -A app.celery worker --loglevel=info