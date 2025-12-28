const { DataTypes } = require("sequelize");
const RbacStore = require("../db");
const User = require("./User");
const Policy = require("./Policy");

const UserPolicyMap = RbacStore.client.define(
  "UserPolicyMap",
  {
    mappingId: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
      allowNull: false,
      field: "mapping_id",
    },
  },
  {
    tableName: "user_policy_mappings",
  }
);

User.belongsToMany(Policy, { through: UserPolicyMap });
Policy.belongsToMany(User, { through: UserPolicyMap });
module.exports = UserPolicyMap;
