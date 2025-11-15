// services/visitor_service.js
const Visitor = require('../models/Visitor');
const axios = require('axios');

async function getCityFromIp(ip) {
  try {
    const response = await axios.get(`https://ipapi.co/${ip}/json/`, { timeout: 1500 });
    if (response.status === 200) {
      return response.data.city || "Inconnue";
    }
  } catch (error) {
    if (error.code === 'ECONNABORTED') {
      // Timeout
      return "Inconnue";
    }
    return "Inconnue";
  }
  return "Inconnue";
}

async function registerVisitor(ip, userAgent) {
  // Anonymisation légère de l'adresse IP (RGPD-friendly)
  if (ip.split('.').length >= 4) {
    const parts = ip.split('.');
    ip = parts.slice(0, 3).join('.') + '.xxx';
  }

  const visitor = Visitor.findByIp(ip);

  // Si c'est une nouvelle IP → nouveau visiteur
  if (!visitor) {
    const city = await getCityFromIp(ip);
    Visitor.create(ip, userAgent, city);
  }
}

function getTotalVisitors() {
  return Visitor.count();
}

module.exports = {
  registerVisitor,
  getTotalVisitors
};

