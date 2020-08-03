FROM python:3.8-slim
RUN apt-get update && apt-get install -y iputils-ping net-tools

# Add docker-compose-wait tool
ENV WAIT_VERSION 2.7.3
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
RUN groupadd -r lupi && useradd --no-log-init -r -g lupi lupi

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt

EXPOSE 5000
USER lupi
CMD /wait && gunicorn -w 4 --bind game_server:8080 game_server.wsgi:app

COPY . /code/game_server
