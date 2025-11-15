// services/create_user.js
const User = require('../models/User');
const crypto = require('crypto');

function createUser(email, passwd) {
  const passwdBuffer = Buffer.from(passwd, 'utf-8');
  const hashOne = crypto.createHash('sha512').update(passwdBuffer).digest('hex');
  
  const existingUser = User.findByEmail(email);
  
  if (existingUser) {
    console.log("Utilisateur déjà existant :", existingUser);
    return existingUser;
  } else {
    const newUser = User.create(email, hashOne, false);
    console.log("Utilisateur ajouté :", newUser);
    return newUser;
  }
}

module.exports = createUser;

