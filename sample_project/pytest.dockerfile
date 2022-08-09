FROM python:3.8-alpine

RUN apk add bash
RUN pip install pytest requests

ADD . /app
WORKDIR /app

RUN chmod +x integration-scripts/wait-for-it.sh

ENTRYPOINT [ "sh", "-c", "integration-scripts/wait-for-it.sh sample_service:5000 && pytest" ]