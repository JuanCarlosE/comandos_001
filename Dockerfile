FROM python:3.11

RUN apt-get update
RUN apt-get install -y libsasl2-dev libssl-dev
RUN pip install -U pip

WORKDIR /usr/src/app
COPY . .
RUN apt-get update && apt-get install -y sudo
RUN sudo apt-get install -y libcairo2 libpango-1.0-0
RUN sudo apt-get install -y libgirepository1.0-dev
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 80

CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:80"]