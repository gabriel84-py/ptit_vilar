// services/auth_user.js
const User = require('../models/User');
const crypto = require('crypto');

function authUser(email, passwdSent) {
  const existingUser = User.findByEmail(email);
  
  if (existingUser) {
    const passwd = Buffer.from(passwdSent, 'utf-8');
    const hashOne = crypto.createHash('sha512').update(passwd).digest('hex');
    
    if (existingUser.hashed_password === hashOne) {
      return true;
    } else {
      return false;
    }
  } else {
    return false;
  }
}

module.exports = authUser;

