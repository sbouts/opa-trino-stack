# Downgrade from 6.0.0 due to
# 'database_id cannot be null' error when adding a database
FROM apache/superset:5.0.0-dev

USER root

COPY ../certs/rootca.crt /usr/local/share/ca-certificates
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE='/usr/local/share/ca-certificates/rootca.crt'

RUN uv pip install --no-cache-dir Flask-OAuthlib Authlib trino[sqlalchemy]

USER superset
WORKDIR /app
