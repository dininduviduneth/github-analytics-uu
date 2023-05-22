FROM python:latest
COPY producer.py /app/
WORKDIR /app
RUN apt-get update
RUN apt-get -y upgrade
RUN apt install -y python3-pip
RUN pip install requests
RUN pip install pulsar-client
CMD ["python", "producer.py"]
