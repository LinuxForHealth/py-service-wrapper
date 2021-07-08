FROM python:3.8-alpine


RUN pip install pytest requests
ADD . /app

WORKDIR /app
ENTRYPOINT [ "pytest" ]