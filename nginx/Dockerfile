# Stage 1: Build NGINX with third-party modules
FROM debian:bullseye as builder

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpcre3 \
    libpcre3-dev \
    libssl-dev \
    zlib1g-dev \
    wget \
    unzip \
    ca-certificates

# Set NGINX version and module to download
ENV NGINX_VERSION 1.24.0
ENV STICKY_MODULE_VERSION 1.2.6

# Download NGINX and third-party module source code
WORKDIR /usr/src
RUN wget http://nginx.org/download/nginx-$NGINX_VERSION.tar.gz \
    && wget https://bitbucket.org/nginx-goodies/nginx-sticky-module-ng/get/$STICKY_MODULE_VERSION.tar.gz \
    && tar -zxvf nginx-$NGINX_VERSION.tar.gz \
    && tar -zxvf $STICKY_MODULE_VERSION.tar.gz

# Build NGINX with the sticky module
WORKDIR /usr/src/nginx-$NGINX_VERSION
RUN ./configure \
    --with-http_ssl_module \
    --add-module=/usr/src/nginx-goodies-nginx-sticky-module-ng-* \
    && make \
    && make install

# Stage 2: Create a lightweight final image
FROM debian:bullseye-slim

# Copy the compiled NGINX binary from the builder stage
COPY --from=builder /usr/local/nginx /usr/local/nginx
COPY --from=builder /etc/ssl/certs /etc/ssl/certs

# Create necessary directories and set permissions
RUN mkdir -p /var/log/nginx /var/cache/nginx /etc/nginx/conf.d \
    && apt-get update && apt-get install -y libpcre3 zlib1g openssl \
    && rm -rf /var/lib/apt/lists/*

# Set NGINX as entrypoint
WORKDIR /usr/local/nginx
CMD ["sbin/nginx", "-g", "daemon off;"]
EXPOSE 80 443
