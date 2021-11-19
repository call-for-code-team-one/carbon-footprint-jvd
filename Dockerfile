FROM python:3.9
MAINTAINER Joëlle Van Damme "joelle.van.damme@be.ey.com"

WORKDIR /app
COPY . /app

RUN python3 -m venv ./venv

# Install dependencies:
COPY requirements.txt .
RUN . /venv/bin/activate && pip install -r requirements.txt

ENTRYPOINT [ "python3" ]
#CMD ["app.py"]
CMD ./venv/bin/activate && exec python app.py