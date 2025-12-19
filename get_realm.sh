#!/bin/bash

docker exec -it opa-trino-stack-keycloak-1 sh -c \
  "cp -rp /opt/keycloak/data/h2 /tmp ; \
  /opt/keycloak/bin/kc.sh export --file /tmp/realm.json --users same_file --realm authz \
    --db dev-file \
    --db-url 'jdbc:h2:file:/tmp/h2/keycloakdb;NON_KEYWORDS=VALUE'"

docker cp opa-trino-stack-keycloak-1:/tmp/realm.json .