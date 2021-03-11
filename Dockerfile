FROM python:3.8.8-slim-buster

WORKDIR /app

# RUN apt-get -y update
# RUN apt-get install -y --fix-missing \
#     build-essential \
#     cmake \
#     gfortran \
#     git \
#     wget \
#     curl \
#     graphicsmagick \
#     libgraphicsmagick1-dev \
#     libatlas-base-dev \
#     libavcodec-dev \
#     libavformat-dev \
#     libgtk2.0-dev \
#     libjpeg-dev \
#     liblapack-dev \
#     libswscale-dev \
#     pkg-config \
#     python3-dev \
#     python3-numpy \
#     software-properties-common \
#     zip \
#     && apt-get clean && rm -rf /tmp/* /var/tmp/*


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ringConnector ringConnector
COPY sample_data data

COPY startDownloadForToday.py .

# CMD ls -al /app
CMD ./startDownloadForToday.py