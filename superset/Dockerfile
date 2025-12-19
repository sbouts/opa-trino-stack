FROM apache/superset:6.0.0-dev

USER root

RUN uv pip install --no-cache-dir Flask-OAuthlib Authlib

USER superset
WORKDIR /app
