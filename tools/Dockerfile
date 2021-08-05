FROM python:3.8-slim-buster
LABEL maintainer="phanith.ken@quad.co.jp"

ARG APP_DIR
ARG PROCUSER
ARG PROCUID
ARG PROCGID
ARG PLATFORM

WORKDIR /var/www/app

COPY tools/docker-entrypoint.sh /docker-entrypoint.sh
COPY tools/requirements.txt /var/www/app/requirements.txt
COPY tools/provision.sh /root/provision.sh
COPY tools/deps.txt /root/deps.txt
COPY tools/system-validation.sh /root/system-validation.sh

# update the package and install dependencies
RUN apt-get update -y
RUN apt-get install curl git dos2unix -y
RUN apt-get install ffmpeg libsm6 libxext6  -y

# dealing with unix line endings
RUN if [ "$PLATFORM" != "arm64" ]; then dos2unix system-validation.sh; fi && \
    chmod +x /root/system-validation.sh && \
    /root/system-validation.sh

# install PPA and xvfb to have a virtual screen and unzip to install the chromedriver
RUN apt-get install -y wget xvfb unzip gnupg2

# install pip3 dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /root

RUN chmod +x /docker-entrypoint.sh && \
    chmod +x /root/provision.sh && \
    /root/provision.sh

RUN usermod -u "$PROCUID" "$PROCUSER" && \
    groupmod -g "$PROCGID" "$PROCUSER"

WORKDIR /var/www/app

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["bash"]