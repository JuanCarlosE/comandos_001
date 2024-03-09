FROM python:3.11

RUN apt-get update
#RUN apt-get install -y libsasl2-dev libssl-dev
#RUN python -m pip wheel --wheel-dir=tmp
#RUN pip install -U pip

WORKDIR /usr/src/app
COPY . .
RUN sudo apt-get update
RUN sudo apt-get install -y libcairo2 libpango-1.0-0
RUN sudo apt-get install -y libgirepository1.0-dev
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8080

CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:8080"]