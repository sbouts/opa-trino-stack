package policies

import data.access
import data.admin
import data.context
import data.trino
import data.users
import future.keywords.contains
import future.keywords.if

default allow = false

# this section handle the policies for `admin` user
allow if {
	# print(input)
	admin.allow_admin
}

# this section handle the policies for regular user
allow if {
	# print(input)
	users.if_user_exists(context.user_id)
	access.allow_resource
}

batch contains i if {
	some i
	raw_resource := input.action.filterResources[i]
	allow with input.action.resource as raw_resource
}

batch contains i if {
	some i
	input.action.operation == trino.operations.filter_columns
	count(input.action.filterResources) == 1
	raw_resource := input.action.filterResources[0]
	count(raw_resource.table.columns) > 0
	new_resources := [
	object.union(raw_resource, {"table": {"column": column_name}}) |
		column_name := raw_resource.table.columns[_]
	]
	allow with input.action.resource as new_resources[i]
}

# rowFilters contains row_filter if {
# 	row_filter := {"expression": "nationkey <> 2"}
# }
# columnMask := column_mask if {
# 	input.context.identity.user != "admin"
# 	input.action.operation == "GetColumnMask"
# 	input.action.resource.column.columnName == "phone"
# 	input.action.resource.column.tableName == "customer"
# 	input.action.resource.column.schemaName == "sf1"
# 	input.action.resource.column.catalogName == "tpch"
# 	column_mask := {"expression": "CAST(CONCAT('XXX-XXX-', substring(phone, -4)) AS VARCHAR(15))"}
# }
