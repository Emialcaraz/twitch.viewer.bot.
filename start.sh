#!/bin/bash

export NETWORK_NAME=deepvision

# Check for NETWORK_NAME network and create it
if [ -z $(docker network ls --filter name=^${NETWORK_NAME}$ --format="{{ .Name }}") ] ; then
    echo "Creating network '$NETWORK_NAME'"
    docker network create ${NETWORK_NAME} ;
fi

# If called with 'build', build the project first
if [[ "$1" == build ]]
then
   docker build -f docker/Dockerfile --tag dv.twitch.viewer:latest .
fi

if [[ "$1" == start ]]
then
   docker network create deepvision; \
   docker-compose -f docker/docker-compose.yml up -d
fi

