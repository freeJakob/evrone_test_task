FROM python:3.7-alpine
RUN pip install --upgrade pip
RUN apk update && apk add make gcc musl-dev libffi-dev postgresql-dev git && rm -rf /var/cache/apk && pip install pipenv

WORKDIR /app
COPY . /app

RUN pipenv install --system --deploy

EXPOSE 8000

WORKDIR /app/evrone_test_task

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "-w 4", "evrone_test_task.wsgi:application"]
