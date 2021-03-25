#!/bin/bash

cd "$(dirname "$0")"

docker push ringface/connector:latest
docker push ringface/createauth:latest

if [ -z ${1+x} ]
  then
  echo "semver is not defined"
  else
  echo "tagging to '$1'"
    docker push ringface/connector:$1
    docker push ringface/createauth:$1
fi