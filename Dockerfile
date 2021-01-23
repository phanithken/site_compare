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

# setup chrome PPA
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
#RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see
#RUN apt-get -y update
#RUN apt-get install -y google-chrome-stable
#
## install manually all the missing libraries
#RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

# install chrome
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# create chromedriver directory
#RUN mkdir $CHROMEDRIVER_DIR

# download and install chromedriver
# TODO: https://gist.github.com/ziadoz/3e8ab7e944d02fe872c3454d17af31a5 (maybe use this in docker-entrypoint.sh)
#RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
#RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

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

# put chromedriver into the PATH
#ENV PATH $CHROMEDRIVER_DIR:$PATH

RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash"]