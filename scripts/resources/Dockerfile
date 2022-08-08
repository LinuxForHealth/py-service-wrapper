FROM python:3.9-alpine

ARG PYWEBWRAPPER_FRAMEWORK
ARG PROJECT_DIST
ARG PROJECT_YAML
ARG PROJECT_ROOT

ADD . /tmp/py-service-wrapper

ENV PYWEBWRAPPER_FRAMEWORK ${PYWEBWRAPPER_FRAMEWORK}
ENV PYWEBWRAPPER_PROJECT_ROOT .
ENV PYWEBWRAPPER_PROJECT_FILE ${PROJECT_YAML}
RUN apk --no-cache add gcc musl-dev
RUN pip install --upgrade pip
RUN cd /tmp/py-service-wrapper && pip install .
RUN cd ${PROJECT_ROOT} && ls -al dist/ && pip install ${PROJECT_DIST}
RUN mkdir /opt/app



WORKDIR /opt/app

RUN cp /tmp/py-service-wrapper/project/${PROJECT_YAML} /opt/app/${PROJECT_YAML}

CMD ["python", "-m", "webwrapper.server"]
