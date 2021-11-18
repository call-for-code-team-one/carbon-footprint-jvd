FROM python:3.9
MAINTAINER Joëlle Van Damme "joelle.van.damme@be.ey.com"

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install --upgrade cython
RUN pip install setuptools wheel
# Install the dependencies
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update && \
    apt-get install -y build-essential libzbar-dev
     && \
    pip install zbar
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD ["app.py"]