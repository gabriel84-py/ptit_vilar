// models/Visitor.js
const db = require('../database');

class Visitor {
  static createTable() {
    db.exec(`
      CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT UNIQUE,
        user_agent TEXT,
        city TEXT,
        first_visit DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
  }

  static findByIp(ipAddress) {
    const stmt = db.prepare('SELECT * FROM visitors WHERE ip_address = ?');
    return stmt.get(ipAddress);
  }

  static create(ipAddress, userAgent, city) {
    const stmt = db.prepare(`
      INSERT INTO visitors (ip_address, user_agent, city, first_visit)
      VALUES (?, ?, ?, datetime('now'))
    `);
    const info = stmt.run(ipAddress, userAgent || null, city || null);
    return { id: info.lastInsertRowid, ip_address: ipAddress, user_agent: userAgent, city };
  }

  static count() {
    const stmt = db.prepare('SELECT COUNT(*) as total FROM visitors');
    return stmt.get().total;
  }
}

// Initialiser la table au chargement
Visitor.createTable();

module.exports = Visitor;

