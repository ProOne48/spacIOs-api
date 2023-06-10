FROM python:3.10-slim
LABEL authors="ProOne48"

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install git wget gnupg1 nano build-essential libssl-dev libffi-dev python-dev && \
    mkdir -p /app

WORKDIR /app
COPY requirements.txt /app

RUN echo "export PYTHONPATH=$PYTHONPATH:/app" > /root/.bashrc

RUN export PYTHONPATH=. && \
    python -m pip install --upgrade pip && \
    pip install "gunicorn==20.0.*" && \
    pip install -r requirements.txt -U

COPY . ./

EXPOSE 5000

RUN chmod a+x ./docker/api.server.sh
CMD sh ./docker/api.server.sh
