# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Configuration for docker-compose-light.yml - disables Redis and uses minimal services

import os
import logging

from typing import Any
from datetime import timedelta

# Import all settings from the main config first
from flask_caching.backends.filesystemcache import FileSystemCache
from flask_appbuilder.security.manager import AUTH_OAUTH
from superset_config import *  # noqa: F403

log_level = os.environ.get("SUPERSET_LOG_LEVEL", "INFO")
logging.basicConfig(level=log_level)
# logging.getLogger('trino.client').setLevel(logging.DEBUG)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

# Override caching to use simple in-memory cache instead of Redis
RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

CACHE_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_light_",
}
DATA_CACHE_CONFIG = CACHE_CONFIG
THUMBNAIL_CACHE_CONFIG = CACHE_CONFIG


# Disable Celery entirely for lightweight mode
CELERY_CONFIG = None  # type: ignore[assignment,misc]


##### OAUTH2 INTEGRATION

# Enable OAuth authentication
AUTH_TYPE = AUTH_OAUTH
LOGOUT_REDIRECT_URL='http://keycloak:8080/realms/authz/protocol/openid-connect/logout'
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = 'Admin'
# OAuth provider configuration for Keycloak
OAUTH_PROVIDERS = [
    {
        'name': 'keycloak',
        'icon': 'fa-key',
        'token_key': 'access_token',  # Keycloak uses 'access_token' for the access token
        'remote_app': {
            'client_id': 'superset',
            'client_secret': 'supersetsupersecret',
            'client_kwargs': {
                'scope': 'openid profile email',
            },
            'api_base_url': 'http://keycloak:8080/realms/authz/protocol/',
            'access_token_url': 'http://keycloak:8080/realms/authz/protocol/openid-connect/token',
            'authorize_url': 'http://localhost:30080/realms/authz/protocol/openid-connect/auth',
            'token_url': 'http://keycloak:8080/realms/authz/protocol/openid-connect/token',
            'jwks_uri': 'http://keycloak:8080/realms/authz/protocol/openid-connect/certs',
            'issuer': 'http://localhost:30080/realms/authz',
        },
    }
]


#### OAUTH2 DATABSE (TRINO)

# Details needed for databases that allows user to authenticate using personal OAuth2
# tokens. See https://github.com/apache/superset/issues/20300 for more information. The
# scope and URIs are usually optional.
# NOTE that if you change the id, scope, or URIs in this file, you probably need to purge  # noqa: E501
# the existing tokens from the database. This needs to be done by running a query to
# delete the existing tokens.
# https://github.com/apache/superset/pull/30081
DATABASE_OAUTH2_CLIENTS: dict[str, dict[str, Any]] = {
    'Trino': {
        'id': 'trino',
        'secret': 'trinosupersecret',
        'scope': 'openid profile email trino',
        'authorization_request_uri': 'http://localhost:30080/realms/authz/protocol/openid-connect/auth',
        'token_request_uri': 'http://keycloak:8080/realms/authz/protocol/openid-connect/token',
        'request_content_type': 'data' # keycloak doesn't accept application/json body.
    }
}

# OAuth2 state is encoded in a JWT using the alogorithm below.
DATABASE_OAUTH2_JWT_ALGORITHM = "HS256"

# By default the redirect URI points to /api/v1/database/oauth2/ and doesn't have to be
# specified. If you're running multiple Superset instances you might want to have a
# proxy handling the redirects, since redirect URIs need to be registered in the OAuth2
# applications. In that case, the proxy can forward the request to the correct instance
# by looking at the `default_redirect_uri` attribute in the OAuth2 state object.
DATABASE_OAUTH2_REDIRECT_URI = "http://localhost:8088/api/v1/database/oauth2/"

# Timeout when fetching access and refresh tokens.
DATABASE_OAUTH2_TIMEOUT = timedelta(seconds=30)
