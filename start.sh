#!/bin/sh
if [ "$IS_SSH" = "true" ]; then
  service ssh start && nginx -g "daemon off;"
else
  nginx -g "daemon off;" &
  java -jar xxl-job-executor-sample-springboot-2.4.0.jar
fi
