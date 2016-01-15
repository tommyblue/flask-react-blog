#!/bin/bash

# Check if react-blog is running and stop it
docker ps | grep react-blog > /dev/null
if [ $? -eq 0 ]; then
    docker stop react-blog
fi

# Check if react-blog was running and delete it
docker ps -a | grep react-blog > /dev/null
if [ $? -eq 0 ]; then
    docker rm react-blog
fi

# Build react-blog
docker build -t tommyblue/react-blog .

# If react-pg isn't running, start it
docker ps | grep react-pg > /dev/null
if [ $? -ne 0 ]; then
    # Check if it was running
    docker ps -a | grep react-pg > /dev/null
    # then start it
    if [ $? -eq 0 ]; then
        docker start react-pg
    else
        docker run --name react-pg -d postgres
    fi
fi

if [ $? -ne 0 ]; then
    echo -e "Unable to start PostgreSQL container"
    exit 1
fi

# Run react-blog
docker run -d -p 3500:3500 -v `pwd`:/srv:ro --name react-blog\
 --link react-pg:postgres tommyblue/react-blog python /srv/server.py
