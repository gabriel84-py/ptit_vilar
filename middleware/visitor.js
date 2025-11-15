// middleware/visitor.js
const { registerVisitor } = require('../services/visitor_service');

async function countUniqueVisitors(req, res, next) {
  const clientIp = req.ip || req.connection.remoteAddress || 'unknown';
  const userAgent = req.get('user-agent') || 'unknown';
  
  // Enregistre uniquement si c'est une IP nouvelle
  await registerVisitor(clientIp, userAgent);
  
  next();
}

module.exports = { countUniqueVisitors };

