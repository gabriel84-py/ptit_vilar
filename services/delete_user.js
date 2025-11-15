// services/delete_user.js
const User = require('../models/User');

function deleteUser(email) {
  const user = User.findByEmail(email);
  
  if (user) {
    User.deleteByEmail(email);
    console.log("🗑️ Utilisateur supprimé :", email);
    return true;
  } else {
    console.log("Utilisateur non trouvé :", email);
    return false;
  }
}

module.exports = deleteUser;

