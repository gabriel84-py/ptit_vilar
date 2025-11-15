// models/User.js
const db = require('../database');

class User {
  static createTable() {
    db.exec(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
      )
    `);
  }

  static findByEmail(email) {
    const stmt = db.prepare('SELECT * FROM users WHERE email = ?');
    const row = stmt.get(email);
    if (!row) return null;
    return {
      ...row,
      is_admin: row.is_admin === 1 || row.is_admin === true
    };
  }

  static create(email, hashedPassword, isAdmin = false) {
    const stmt = db.prepare('INSERT INTO users (email, hashed_password, is_admin) VALUES (?, ?, ?)');
    const info = stmt.run(email, hashedPassword, isAdmin ? 1 : 0);
    return { id: info.lastInsertRowid, email, hashed_password: hashedPassword, is_admin: isAdmin };
  }

  static deleteByEmail(email) {
    const stmt = db.prepare('DELETE FROM users WHERE email = ?');
    return stmt.run(email);
  }

  static findAll() {
    const stmt = db.prepare('SELECT * FROM users');
    const results = stmt.all();
    return results.map(row => ({
      ...row,
      is_admin: row.is_admin === 1 || row.is_admin === true
    }));
  }
}

// Initialiser la table au chargement
User.createTable();

module.exports = User;

