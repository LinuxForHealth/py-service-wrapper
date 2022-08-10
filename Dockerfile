from python:3.9-alpine

ADD . /tmp/py-service-wrapper

RUN apk add docker

WORKDIR /tmp/py-service-wrapper

CMD ["/bin/sh", "scripts/build-docker.sh"]