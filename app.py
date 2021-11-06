from flask import Flask, render_template, request
from celery import Celery
import time
import json

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'] , broker=app.config['CELERY_BROKER_URL'])
celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'] , broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)


@celery.task
def background_task(a, b):
    # time.sleep(2)
    print("Background Task Called!")
    response = {"Result" : str(a+b)}
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/task")
def task():
    response = {}
    task = background_task.delay(3, 4)
    # task = celery.send_task('tasks.background_task', kwargs={ 'a': 3, 'b': 4 })
    # while(not task.ready()):
    #     time.sleep(1)
    # response['result'] = str(task.get(timeout=5))
    response['result'] = str(task.get()) # (frowned upon) turn this async operation back into sync and retrieve result before returning from route

    response['Message'] = 'Hello Client!'
    return json.dumps(response)

@app.route("/task_status/<task_id>")
def task_status(task_id):
    status = celery.AsyncResult(task_id, app=celery)
    return str(status.state)

@app.route("/task_result/<task_id>")
def task_result(task_id):
    result = celery.AsyncResult(task_id).result
    return str(result)


if __name__ == '__main__':
    app.run(debug=True)
