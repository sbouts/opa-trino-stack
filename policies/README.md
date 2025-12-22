# OPA Policies

## Directory Structure

```shell
.
├── access
│   ├── allow_default_acces.rego
│   ├── allow_resource_catalog.rego
│   ├── allow_resource_column.rego
│   ├── allow_resource_schema.rego
│   ├── allow_resource_table.rego
│   ├── allow_resource.rego
│   └── main.rego
├── admin
│   └── main.rego
├── context
│   ├── input_action.rego
│   └── input_context.rego
├── db
│   └── main.rego
├── trino
│   ├── operations.rego
│   ├── schema.rego
│   └── table.rego
├── users
│   └── main.rego
├── validations
│   ├── catalog.rego
│   ├── column.rego
│   ├── schema.rego
│   └── table.rego
├── main.rego
└── README.md
```

## References

- [Trino OPA Policies](https://github.com/nil1729/trino-opa-policy)
- [Trino OPA Example](https://github.com/DragonPomelo/trino-opa-example)
