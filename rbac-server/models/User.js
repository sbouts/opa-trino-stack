const { DataTypes } = require("sequelize");
const RbacStore = require("../db");

const User = RbacStore.client.define(
  "User",
  {
    name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    email: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true,
    },
    isAdmin: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
      allowNull: false,
      field: "is_admin",
    },
    userId: {
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true,
      field: "user_id",
      autoIncrement: true,
    },
  },
  {
    tableName: "users",
  }
);

module.exports = User;
