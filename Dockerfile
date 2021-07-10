# syntax=docker/dockerfile:1

FROM daocloud.io/atsctoo/python3.8.2-ubuntu18.04:latest

WORKDIR /usr/tanly/app/

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:8000","-k","gevent", "-t", "300", "--access-logfile", "-", "learning_log.wsgi:application"]

