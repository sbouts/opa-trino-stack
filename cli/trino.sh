#!/bin/bash

DOCKER_NETWORK="authz_net"

VERSION=479
SERVER="https://trino_proxy"

if [ -z "${1}" ]; then
  echo "Expected arguments."
  echo "  Usage: ./trino.sh <args>"
  exit 1
fi

echo docker run --network=${DOCKER_NETWORK} -it trinodb/trino:${VERSION} trino "${SERVER}" --insecure ${1}
