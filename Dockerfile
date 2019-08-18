FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
RUN mkdir /src
RUN mkdir /static
ADD ./static /static
ADD ./src /src
ADD /src/requirements.txt /src/
ADD django.conf /
RUN pip install --upgrade pip
RUN pip install -r /src/requirements.txt
WORKDIR /src
CMD python manage.py collectstatic --no-input;python manage.py makemigrations;python manage.py migrate;gunicorn -w 4 -b 0.0.0.0:8080 application.wsgi:application --timeout 300
