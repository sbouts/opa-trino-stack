const User = require("../models/User");
const Policy = require("../models/Policy");
const asyncHandler = require("../middleware/asyncHandler");

// associate a policy with a user
exports.associatePolicyWithUser = asyncHandler(async (req, res) => {
  const user = await User.findByPk(req.body.userId);
  if (!user) {
    throw new Error("user not found");
  }
  const policy = await Policy.findByPk(req.body.policyId);
  if (!policy) {
    throw new Error("policy not found");
  }
  user.addPolicy(policy);
  res.status(201).json({ user, policy });
});

// get all policies for a user
exports.getPoliciesByUser = asyncHandler(async (req, res) => {
  const user = await User.findByPk(req.params.userId);
  if (!user) {
    throw new Error("User not found");
  }
  const policies = [];
  const userPolicies = await user.getPolicies();
  policies.push(...userPolicies);
  res.status(200).json(policies);
});

// get all policies for a user
// exports.getPoliciesByUser = asyncHandler(async (req, res) => {
//   const user = await User.findByPk(req.params.userId);
//   if (!user) {
//     throw new Error("User not found");
//   }
//   const groups = await user.getGroups();
//   const policies = [];
//   for (const group of groups) {
//     const groupPolicies = await group.getPolicies();
//     policies.push(...groupPolicies);
//   }
//   res.status(200).json(policies);
// });

