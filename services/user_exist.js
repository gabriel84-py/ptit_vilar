// services/user_exist.js
const User = require('../models/User');

function userExist(email) {
  const existingUser = User.findByEmail(email);
  return !!existingUser;
}

module.exports = userExist;

