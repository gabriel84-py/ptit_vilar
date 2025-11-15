// middleware/auth.js
const serializer = require('../utils/cookie-signer');

function requireLogin(req, res, next) {
  const token = req.cookies?.auth;
  
  if (!token) {
    return res.redirect('/login');
  }
  
  try {
    // Décoder le cookie signé (équivalent à itsdangerous)
    const data = serializer.loads(token);
    if (!data.is_admin) {
      return res.status(403).send('Accès refusé');
    }
    
    req.user = data;
    next();
  } catch (error) {
    return res.redirect('/login');
  }
}

function loadUserFromCookie(req, res, next) {
  req.user = null;
  const token = req.cookies?.auth;
  
  if (token) {
    try {
      req.user = serializer.loads(token);
    } catch (error) {
      // Ignorer les erreurs de signature
    }
  }
  
  next();
}

module.exports = { requireLogin, loadUserFromCookie };

