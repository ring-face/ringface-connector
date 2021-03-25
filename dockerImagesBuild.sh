#!/bin/bash

cd "$(dirname "$0")"

docker build . --tag ringface/connector:latest
docker build -f Dockerfile.createauth . --tag ringface/createauth:latest

if [ -z ${1+x} ]
  then
  echo "semver is not defined"
  else
  echo "tagging to '$1'"
  docker tag ringface/connector:latest ringface/connector:$1
  docker tag ringface/createauth:latest ringface/createauth:$1
fi