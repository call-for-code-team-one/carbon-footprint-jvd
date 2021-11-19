FROM python:3.9
MAINTAINER Joëlle Van Damme "joelle.van.damme@be.ey.com"

WORKDIR /app
COPY . /app

RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install pyzbar

CMD . venv/bin/activate && exec python app.py

