#!/bin/bash

docker build . --tag ringface/connector:latest
docker build -f Dockerfile.createauth . --tag ringface/createauth:latest