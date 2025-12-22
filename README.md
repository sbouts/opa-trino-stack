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
