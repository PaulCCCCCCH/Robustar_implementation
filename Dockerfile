FROM leonleyang/robustar-base:base-0.3.2
# Default VCUDA is 11.1
ARG VCUDA=11.1 
COPY . /Robustar2/

WORKDIR /Robustar2

## Host with lerna: Install global node dependencies
# RUN npm install -g webpack webpack-cli lerna @vue/cli

# Install PyTorch
RUN chmod +x ./scripts/install_pytorch.sh
RUN ["/bin/bash", "-c", "./scripts/install_pytorch.sh -c $VCUDA"]

## Host with NGINX: 
RUN rm -rf /var/www/html
RUN cp -r /Robustar2/front-end/packages/robustar/dist /var/www/html
COPY deployment/nginx.conf /etc/nginx/sites-enabled/default

# Start server
CMD ["/bin/bash", "./scripts/start.sh"]

