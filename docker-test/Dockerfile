FROM paulcccccch/robustar-base:base-0.2.0
COPY test-data/Robustar2 .
COPY .. /Robustar2/

WORKDIR /Robustar2

# Install backend test environment
RUN chmod +x ./scripts/install_pytorch.sh
RUN ["/bin/bash", "-c", "./scripts/install_pytorch.sh -c cpu"]
RUN pip install pytest
RUN pip install protobuf==3.20.* 

# Install frontend test environment
RUN curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -
RUN sudo apt-get install -y nodejs
# Following suggested by https://docs.cypress.io/guides/continuous-integration/introduction#Dependencies
RUN DEBIAN_FRONTEND=noninteractive sudo apt-get install -y libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb
RUN npm install --save-dev cypress 


## Host with NGINX: 
RUN rm -rf /var/www/html
RUN cp -r /Robustar2/front-end/packages/robustar/dist /var/www/html



# Start server
CMD ["/bin/bash", "./scripts/start.sh"]

