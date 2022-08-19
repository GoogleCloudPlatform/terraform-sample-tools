# Docker from https://github.com/antlr/antlr4/tree/master/docker
FROM antlr/antlr4

# Install Python 3.9.5
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Developer Tools
RUN apk update && apk add bash

WORKDIR /app
COPY . /app
RUN run.sh

# RUN apt install default-jre -y
#docker build -t tftools:latest .
#docker run -it  tftools:latest
ENTRYPOINT ["/bin/sh"]