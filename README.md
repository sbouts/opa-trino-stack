# Keycloak - Trino - Opal - Postgres

## TODO

* Limit access of regularman to trino's builtin `tpch/tiny` schema only using OPA
* Add postgres database (with mock data)

## Prep

* Have `mkcert` installed
* Copy the mkcert root ca to `./certs/rootca.crt`
    * `cp "$(mkcert -CAROOT)/rootCa.pem" ./certs/rootca.crt`
* Create client cert and key for use in nginx and copy output to `./certs/nginx.crt` and `./certs/nginx.key`
    * `mkcert trino_proxy localhost 127.0.0.1`

## Keycloak + Trino

The following URLs are available:
* Trino UI: [https://localhost/ui/](https://localhost/ui/)
* Keycloak UI: [http://localhost:30080](http://localhost:30080)

Login to Trino as:

* Username: `superman`
* Password: `superman`

* Username: `regularman`
* Password: `regularman`

You can also login to Keycloak using:
* Username: `admin`
* Password: `admin`

The Keycloak Realm "authz" is pre-configured.

## Superset

The following URLs are available:

* Superset UI: [http://localhost:8088](http://localhost:8088)

Changes to make Oauth2 (Keycloak) work:
* Create custom image with Appbuilder for oauth2
* Add `superset_config.py` and `superset_config_docker_light` to include oauth2 config
    * Make sure the `client_id` is the same as the oauth2 client used in Trino
    * Make sure the `trino` scope configured on the trino client in Keycloak is also included
* Create `superset` client in Keycloak
* Set Frontend URL of Keycloak Realm to `http://localhost:30080`

### Connection to Trino using GUI

* URI: `trino://trino_proxy:443/system`
* Check `Impersonate user ..`
* Engine: `{"connect_args":{"http_scheme":"https","verify":false}}`

## OPAL

### TODO

* Get data from e.g. Keycloak??
    * Create RBAC API

### OPAL Server

```shell
# get all policy-data
curl http://localhost:7002/policy-data
```

### OPAL Client (OPA)

```shell
# check opa policies
curl -s -XGET -H 'Content-Type: application/json' 'http://localhost:8181/v1/policies' | jq .

# check opa data
curl -s -XGET -H 'Content-Type: application/json' 'http://localhost:8181/v1/data' | jq .
```

# RBAC Server

## TODO

* Assign policies to user not just groups
* Remove group option because we only want to have user-policy mapping?

## Init

```shell
# create user
curl -XPOST 'http://localhost:5050/api/v1/users' -H "Content-Type: application/json" \
--data-raw '{
    "name": "regularman",
    "email": "regular@man.org",
    "is_admin": false
}'

# get user
curl 'http://localhost:5050/api/v1/users' -H "Content-Type: application/json"

# create policies
# 1
curl -XPOST 'http://localhost:5050/api/v1/policies' -H "Content-Type: application/json" \
--data '{
    "clusterId": 1,
    "name": "policy1",
    "catalog": "tpch",
    "schema": "sf1",
    "table": "customer",
    "columns": ["custkey", "nationkey"]
}'

# 2
curl -XPOST 'http://localhost:5050/api/v1/policies' -H "Content-Type: application/json" \
--data '{
    "clusterId": 1,
    "name": "policy2",
    "catalog": "tpch",
    "schema": "tiny",
    "table": "*",
    "columns": ["*"]
}'

# get policy
curl 'http://localhost:5050/api/v1/policies' -H "Content-Type: application/json"

# assign policies to user
# 1
curl -XPOST 'http://localhost:5050/api/v1/user-policies' -H "Content-Type: application/json" \
--data '{
    "userId": 1,
    "policyId": 1
}'

# 2
curl -XPOST 'http://localhost:5050/api/v1/user-policies' -H "Content-Type: application/json" \
--data '{
    "userId": 1,
    "policyId": 2
}'

# get policies for user
curl 'http://localhost:5050/api/v1/user-policies/1' -H "Content-Type: application/json"

# get opal formatted policies
curl 'http://localhost:5050/api/v1/opal/users/1' -H "Content-Type: application/json"
```

### Links

* [OPA Api Reference](https://www.openpolicyagent.org/docs/rest-api)
* [OPAL config reference](https://opal.ac/getting-started/configuration)
* [OPAL policies example](https://github.com/permitio/opal-example-policy-repo/tree/master)
* [Trino OPA example](https://github.com/nil1729/trino-opa-demo)
* [Trino Request Input examples](https://github.com/lakekeeper/lakekeeper/tree/main/authz/opa-bridge/inputs)
* [Make external requests example](https://github.com/lakekeeper/lakekeeper/blob/main/authz/opa-bridge/policies/lakekeeper/authentication.rego)