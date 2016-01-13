FROM ubuntu:14.04
MAINTAINER Tommaso Visconti <tommyblue@develer.com>
RUN test -d /srv || mkdir /srv/
WORKDIR /srv
RUN apt-get update && apt-get install -y python-pip libpq-dev python-dev
COPY requirements.txt /srv/
RUN pip install -r /srv/requirements.txt
