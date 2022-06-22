FROM ubuntu:20.04 as ubuntu
ARG NODEJS_MAJOR_VERSION=14
ENV DEBIAN_FRONTEND=nonintercative
RUN apt-get update && apt-get install curl pip python3.9-venv python3.9-distutils sudo git lsb-core -y && \
    curl --proto '=https' --tlsv1.2 -sSf -L https://deb.nodesource.com/setup_${NODEJS_MAJOR_VERSION}.x | bash - &&\
    apt-get install nodejs -y

FROM ubuntu as cat-addresses-base
WORKDIR /app
COPY . /app/

# CHIA BUILD STEP
FROM cat-addresses-base as cat-addresses
ENV PATH=/chia-blockchain/venv/bin:$PATH
ENV CHIA_ROOT=/root/.chia/mainnet
ENV keys="generate"
ENV service="node"
ENV testnet="false"
ENV TZ="UTC"
ENV upnp="true"
ENV log_to_file="true"
ENV healthcheck="false"

WORKDIR /chia-blockchain
ARG BRANCH=fc.block_spends_and_ws_updates
ARG COMMIT=""

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    lsb-release sudo

# todo: update to official git repo - on my personal repo to use a branch that contains required changes that haven't been merged yet
RUN echo "cloning ${BRANCH}" && \
    git clone --branch ${BRANCH} --recurse-submodules=mozilla-ca https://github.com/freddiecoleman/chia-blockchain . && \
    # If COMMIT is set, check out that commit, otherwise just continue
    ( [ ! -z "$COMMIT" ] && git checkout $COMMIT ) || true && \
    echo "running build-script" && \
    /bin/sh ./install.sh
WORKDIR /app
RUN python3 setup.py install
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y tzdata curl && \
    rm -rf /var/lib/apt/lists/* && \
    ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime && echo "$TZ" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata
RUN chmod +x /app/docker-entrypoint.sh && chmod +x /app/docker-start.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["/app/docker-start.sh"]