FROM paulcccccch/robustar:base-0.1.0
# Default VCUDA is 11.1
ARG VCUDA=11.1 
COPY . /Robustar2/

WORKDIR /Robustar2
RUN file="$(ls -1 ./scripts/)" && echo $file


## Host with lerna: Install global node dependencies
# RUN npm install -g webpack webpack-cli lerna @vue/cli

## Host with NGINX: 
RUN rm -rf /var/www/html
RUN cp -r /Robustar2/front-end/packages/robustar/dist /var/www/html


# Install PyTorch 
RUN ["/bin/bash", "-c", "./scripts/install_pytorch.sh -c $VCUDA"]

CMD ["/bin/bash", "./scripts/start.sh"]

