#!/bin/bash

curl -XPOST 'http://localhost:5050/api/v1/users' -H "Content-Type: application/json" \
--data-raw '{
    "name": "regularman",
    "email": "regular@man.org",
    "is_admin": false
}'

sleep 1

curl -XPOST 'http://localhost:5050/api/v1/users' -H "Content-Type: application/json" \
--data-raw '{
    "name": "superman",
    "email": "super@man.org",
    "is_admin": true
}'

sleep 1

curl -XPOST 'http://localhost:5050/api/v1/policies' -H "Content-Type: application/json" \
--data '{
    "clusterId": 1,
    "name": "policy1",
    "catalog": "tpch",
    "schema": "sf1",
    "table": "customer",
    "columns": ["custkey", "nationkey"]
}'

sleep 1

curl -XPOST 'http://localhost:5050/api/v1/user-policies' -H "Content-Type: application/json" \
--data '{
    "userId": 1,
    "policyId": 1
}'

curl -XPOST 'http://localhost:5050/api/v1/user-policies' -H "Content-Type: application/json" \
--data '{
    "userId": 2,
    "policyId": 1
}'