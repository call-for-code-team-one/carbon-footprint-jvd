FROM python:3.9-alpine

WORKDIR /carbon_footprint_app-jvd

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN pip install --upgrade pip
RUN pip install --upgrade cython
RUN pip install setuptools wheel

ENV OPENCV_VERSION=3.4.1

RUN echo -e '@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing\n\
http://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories

RUN apk add -U \
      --virtual .build-dependencies \
        build-base \
        openblas-dev \
        unzip \
        wget \
        cmake \
        # accelerated baseline JPEG compression and decompression library
        libjpeg-turbo-dev \
        # Portable Network Graphics library
        libpng-dev \
        # A software-based implementation of the codec specified in the emerging JPEG-2000 Part-1 standard (development files)
        # Provides support for the Tag Image File Format or TIFF (development files)
        tiff-dev \
        # Libraries for working with WebP images (development files)
        libwebp-dev \
    && pip install numpy \
    && cd /carbon_footprint_app-jvd \
    && wget --quiet https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip \
    && unzip ${OPENCV_VERSION}.zip \
    && rm -rf ${OPENCV_VERSION}.zip \
    && mkdir -p /carbon_footprint_app-jvd/opencv-${OPENCV_VERSION}/build \
    && cd /carbon_footprint_app-jvd/opencv-${OPENCV_VERSION}/build \
    && cmake \
      -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D WITH_FFMPEG=NO \
      -D WITH_IPP=NO \
      -D WITH_OPENEXR=NO \
      -D WITH_TBB=YES \
      -D BUILD_EXAMPLES=NO \
      -D BUILD_ANDROID_EXAMPLES=NO \
      -D INSTALL_PYTHON_EXAMPLES=NO \
      -D BUILD_DOCS=NO \
      -D BUILD_opencv_python2=NO \
      -D BUILD_opencv_python3=ON \
      -D PYTHON3_EXECUTABLE=/usr/local/bin/python \
      -D PYTHON3_INCLUDE_DIR=/usr/local/include/python3.6m/ \
      -D PYTHON3_LIBRARY=/usr/local/lib/libpython3.so \
      -D PYTHON_LIBRARY=/usr/local/lib/libpython3.so \
      -D PYTHON3_PACKAGES_PATH=/usr/local/lib/python3.6/site-packages/ \
      -D PYTHON3_NUMPY_INCLUDE_DIRS=/usr/local/lib/python3.6/site-packages/numpy/core/include/ \
      .. \
    && make VERBOSE=1 \
    && make install \
    && rm -rf /carbon_footprint_app-jvd/opencv-${OPENCV_VERSION} \
    && apk del .build-dependencies \
    && rm -rf /var/cache/apk/*
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000
COPY . .
CMD ["flask", "run","app.py"]