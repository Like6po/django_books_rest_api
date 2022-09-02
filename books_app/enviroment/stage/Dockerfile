FROM python:3.10

RUN pip install --upgrade pip
RUN mkdir /root/django
WORKDIR ./root/django
COPY ./books_app/enviroment/stage/requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt
WORKDIR /root/django/books_app
COPY ./books_app ./
RUN rm -r enviroment
COPY ./books_app/enviroment/stage/settings.py ./books_app/settings.py
