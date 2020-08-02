FROM python:3.8-slim
RUN apt-get update && apt-get install -y iputils-ping net-tools

# Add docker-compose-wait tool
ENV WAIT_VERSION 2.7.3
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

WORKDIR /code
EXPOSE 5000
RUN pip install flask
COPY . /code/ui
CMD /wait && python3 -m ui.app  # should be gunicorn
