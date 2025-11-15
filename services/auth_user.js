// services/auth_user.js
const User = require('../models/User');
const crypto = require('crypto');

async function authUser(email, passwdSent) {
  const existingUser = await User.findByEmail(email); // <-- await important

  if (!existingUser) return false;

  // logging utile pour debug
  console.log('User found:', !!existingUser);
  console.log('Stored hash:', existingUser.hashed_password);

  const hashOne = crypto.createHash('sha512').update(passwdSent, 'utf8').digest('hex');
  console.log('Computed hash:', hashOne);

  return existingUser.hashed_password === hashOne;
}

module.exports = authUser;
