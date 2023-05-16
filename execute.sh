#!/usr/bin/env sh
docker-compose down \
&& if [[ -n $(docker images | grep "automation-test" | awk '{print $3}') ]]; then docker rmi $(docker images | grep "automation-test" | awk '{print $3}'); fi \
&& docker-compose up -d
