# Keycloak - Trino - Opal - Postgres

## INFO
The following additional sites are available:

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

Changes to make Oauth2 (Keycloak) work:
* Create custom image with Appbuilder for oauth2
* Add `superset_config.py` and `superset_config_docker_light` to include oauth2 config
* Create `superset` client in Keycloak
* Set Frontend URL of Keycloak Realm to `http://localhost:30080`
