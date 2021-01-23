FROM python:3.8-slim-buster

# defined in docker-compose.yml
ARG CHROMEDRIVER_DIR

WORKDIR /code

COPY requirements.txt .

# update the package and install dependencies
RUN apt-get update -y
RUN apt-get install curl -y
RUN apt-get install ffmpeg libsm6 libxext6  -y

# install PPA and xvfb to have a virtual screen and unzip to install the chromedriver
RUN apt-get install -y wget xvfb unzip gnupg2

# Install Chrome WebDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    mkdir -p $CHROMEDRIVER_DIR && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d $CHROMEDRIVER_DIR && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x $CHROMEDRIVER_DIR/chromedriver && \
    ln -fs $CHROMEDRIVER_DIR/chromedriver /usr/local/bin/chromedriver

# Install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash"]