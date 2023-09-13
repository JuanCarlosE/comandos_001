FROM python:3.11

RUN apt-get update
RUN apt-get install -y libsasl2-dev libssl-dev
#RUN python -m pip wheel --wheel-dir=tmp

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install -U pip
RUN pip install -r requirements.txt
COPY . . 

EXPOSE 8000

CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:8000"]