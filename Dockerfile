FROM python:3.9-alpine

WORKDIR /carbon_footprint_app-jvd

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN pip install --upgrade pip
RUN pip install --upgrade cython
RUN pip install setuptools wheel
RUN apk add gcc g++ linux-headers musl-dev git && pip install git+https://github.com/pandas-dev/pandas
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers && pip install Pillow
COPY requirements.txt requirements.txt
RUN echo -e '@edgunity http://nl.alpinelinux.org/alpine/edge/community\n\
@edge http://nl.alpinelinux.org/alpine/edge/main\n\
@testing http://nl.alpinelinux.org/alpine/edge/testing\n\
@community http://dl-cdn.alpinelinux.org/alpine/edge/community'\
  >> /etc/apk/repositories

RUN apk add --update --no-cache \
  # --virtual .build-deps \
      build-base \
      openblas-dev \
      unzip \
      wget \
      cmake \

      #Intel® TBB, a widely used C++ template library for task parallelism'
      libtbb@testing  \
      libtbb-dev@testing   \

      # Wrapper for libjpeg-turbo
      libjpeg  \

      # accelerated baseline JPEG compression and decompression library
      libjpeg-turbo-dev \

      # Portable Network Graphics library
      libpng-dev \


      # Provides support for the Tag Image File Format or TIFF (development files)
      tiff-dev \

      # Libraries for working with WebP images (development files)
      libwebp-dev \

      # A C language family front-end for LLVM (development files)
      clang-dev \

      linux-headers \

      && pip install numpy

ENV CC /usr/bin/clang
ENV CXX /usr/bin/clang++

ENV OPENCV_VERSION="4.5.1"

RUN echo -e '@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing\n\
http://dl-cdn.alpinelinux.org/alpine/edge/community' >> /etc/apk/repositories

RUN apk add -U \
      # --virtual .runtime-dependencies \
        #Intel® TBB, a widely used C++ template library for task parallelism'
        libtbb@testing \
        libtbb-dev@testing \
        # Wrapper for libjpeg-turbo
        libjpeg  \
        openblas \
        jasper \
    && apk add -U \
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
        jasper-dev \
        # Provides support for the Tag Image File Format or TIFF (development files)
        tiff-dev \
        # Libraries for working with WebP images (development files)
        libwebp-dev \
        # A C language family front-end for LLVM (development files)
        clang-dev \
        linux-headers \
    && pip install numpy \
    && mkdir /opt \
    && cd /opt \
    && wget --quiet https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip \
    && unzip ${OPENCV_VERSION}.zip \
    && rm -rf ${OPENCV_VERSION}.zip \
    && mkdir -p /opt/opencv-${OPENCV_VERSION}/build \
    && cd /opt/opencv-${OPENCV_VERSION}/build \
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
    && make \
    && make install \
    && rm -rf /opt/opencv-${OPENCV_VERSION} \
    && apk del .build-dependencies \
    && rm -rf /var/cache/apk/*
RUN pip install -r requirements.txt

EXPOSE 5000
COPY . .
CMD ["flask", "run","app.py"]