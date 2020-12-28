FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y libgl1-mesa-dev libgl1-mesa-glx
RUN apt-get install -y libgtk2.0-dev
COPY . /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt

CMD [ "python3", "./app.py" ]