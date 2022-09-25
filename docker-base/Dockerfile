FROM ubuntu:20.04
RUN mkdir /Robustar2
WORKDIR /Robustar2

# update and install env dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install curl sudo python3.9 python3-pip

## We use NGINX for production. Node no longer needed.
# RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
# RUN sudo apt-get install nodejs -y
RUN apt-get -y install nginx

# alias
RUN echo 'alias python=python3.9'>>~/.bashrc

# update pip
RUN python3.9 -m pip install --upgrade --force-reinstall pip

# move requirements
ADD requirements.txt .

# Python libs
RUN python3.9 -m pip install -r requirements.txt