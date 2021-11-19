FROM python:3.9
MAINTAINER Joëlle Van Damme "joelle.van.damme@be.ey.com"

WORKDIR /app
COPY . /app
ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/Scripts:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD ["app.py"]