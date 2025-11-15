// services/view_users.js
const User = require('../models/User');

function getAllUsers() {
  return User.findAll();
}

module.exports = { getAllUsers };

