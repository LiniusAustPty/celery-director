Tests
=====

To test Celery Director in real conditions we decided to use an executing `worker` :

```
$ (venv) git clone https://github.com/ovh/director && cd director
$ (venv) python setup.py develop
$ (venv) export DIRECTOR_HOME=`pwd`/tests/workflows/
$ (venv) docker-compose up -d redis postgres
$ (venv) director celery worker --pool=solo --queues=celery,complex
```

Configuration (database, redis...) can be customized in the `$DIRECTOR_HOME/.env` file.

```
# postgres director database uri
DIRECTOR_DATABASE_URI=postgresql://postgres_user:postgres_pass@localhost:5432/director_db
# redis celery broker database uri
DIRECTOR_BROKER_URI=redis://localhost:6379/0
```

You can then launch the tests in another terminal :

```
$ pip install pytest==5.3.5
$ pytest tests/ -v
```

kill all celery workers :

```
$ pkill -9 -f 'celery'
```
