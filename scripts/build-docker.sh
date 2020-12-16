#!/bin/sh

cd /tmp/py-service-wrapper
cp -r ${PROJECT_ROOT} ./project/

docker build --file scripts/resources/Dockerfile \
             --build-arg PYWEBWRAPPER_FRAMEWORK=${PYWEBWRAPPER_FRAMEWORK} \
             --build-arg PROJECT_ROOT=/tmp/py-service-wrapper/project \
             --build-arg PROJECT_DIST=${PROJECT_DIST} \
             --build-arg PROJECT_YAML=${PROJECT_YAML} \
             -t ${IMAGE_NAME} .
