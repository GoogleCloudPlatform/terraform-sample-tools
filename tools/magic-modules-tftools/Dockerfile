# Docker from https://github.com/antlr/antlr4/tree/master/docker
#FROM antlr/antlr4
FROM msampathkumar/antlr_antlr4

# Install Python 3.9.5
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Developer Tools
RUN apk update && apk add bash

WORKDIR /magic-modules-tftools
COPY . /magic-modules-tftools
RUN sh run.sh

WORKDIR /root

ENTRYPOINT ["/bin/sh"]

## Docker commands ##
# docker build -t tftools:latest .
# docker run -it  tftools:latest
# docker tag tftools:latest msampathkumar/tftools
# docker push msampathkumar/tftools

# docker pull msampathkumar/tftools
# docker run -it msampathkumar/tftools