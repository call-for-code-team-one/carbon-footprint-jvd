FROM python:3.9
MAINTAINER Joëlle Van Damme "joelle.van.damme@be.ey.com"

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install --upgrade cython
RUN pip install setuptools wheel
RUN apt-get update -y
RUN apt-update && apt install -y libsm6 libxext6 
# Install the dependencies
RUN apt-get update && \
    apt-get install -y build-essential libzbar-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD ["app.py"]