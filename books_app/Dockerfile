FROM python:3.10

RUN pip install --upgrade pip
WORKDIR /books_app
COPY requirements.txt /books_app
RUN pip install -r requirements.txt
COPY . .