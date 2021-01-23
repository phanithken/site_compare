FROM python:3.8-slim-buster

WORKDIR /code

COPY requirements.txt .

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash"]