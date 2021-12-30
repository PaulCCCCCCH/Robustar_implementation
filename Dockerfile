FROM paulcccccch/robustar:base-0.0.1
# Default VCUDA is 11.1
ARG VCUDA=11.1 
COPY . /Robustar2/

WORKDIR /Robustar2


## Host with lerna: Install global node dependencies
# RUN npm install -g webpack webpack-cli lerna @vue/cli

## Host with NGINX: 
RUN sudo apt-get -y install nginx
RUN rm -rf /var/www/html
RUN cp -r /Robustar2/front-end/packages/robustar/dist /var/www/html

# Install PyTorch 
RUN ["/bin/bash", "-c", "./scripts/install_pytorch.sh -c $VCUDA"]

# Install frontend libraries
# WORKDIR /Robustar2/front-end
# RUN npm install
# RUN lerna bootstrap

# Build image-editor
# RUN lerna run build:editor
# WORKDIR /Robustar2

CMD ["/bin/bash", "./scripts/start.sh"]

