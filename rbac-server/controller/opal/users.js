const User = require("../../models/User");
const asyncHandler = require("../../middleware/asyncHandler");
const {
  createCatalogAccess,
  createSchemaAccess,
  createTableAccess,
  createColumnAccess,
} = require("./utils");

exports.getUserPolicies = asyncHandler(async (req, res) => {
  const clusterId = req.params.clusterId;
  const users = await User.findAll();

  const opaUsers = [];
  const catalogAccess = [];
  const schemaAccess = [];
  const tableAccess = [];
  const columnAccess = [];

  for (const user of users) {
    const policies = [];

    // users
    const userPolicies = await user.getPolicies({ where: { clusterId } });
    policies.push(...userPolicies);
    console.log(userPolicies.length);

    // groups
    const groups = await user.getGroups();
    for (const group of groups) {
      const groupPolicies = await group.getPolicies({ where: { clusterId } });
      policies.push(...groupPolicies);
    }
    if (policies.length === 0) {
      continue;
    } else {
      opaUsers.push({ [user.name]: { "is_admin": user.isAdmin } });
      catalogAccess.push(createCatalogAccess(policies, "user", user.name));
      schemaAccess.push(createSchemaAccess(policies, "user", user.name));
      tableAccess.push(createTableAccess(policies, "user", user.name));
      columnAccess.push(createColumnAccess(policies, "user", user.name));
    }
  }

  res.status(200).json({
    users: opaUsers,
    catalog: catalogAccess,
    schema: schemaAccess,
    table: tableAccess,
    column: columnAccess,
  });
});
