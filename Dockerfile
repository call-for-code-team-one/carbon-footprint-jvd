FROM python:3.9

COPY requirements.txt requirements.txt

WORKDIR /carbon_footprint_app-jvd

RUN apk --update add python py-pip openssl ca-certificates py-openssl wget bash linux-headers
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install --upgrade pipenv\
  && pip install --upgrade -r requirements.txt\
  && apk del build-dependencies

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]