#!/usr/bin/bash

VERSION=$1

docker build -t lights_api . && \
docker tag lights_api eliharper/lights_api:$VERSION && \
docker push eliharper/lights_api:$VERSION