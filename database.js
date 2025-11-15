// database.js
const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const BASE_DIR = __dirname;
const DATA_DIR = path.join(BASE_DIR, "data");
const DB_PATH = path.join(DATA_DIR, "app.db");

// Créer le dossier data s'il n'existe pas
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Créer la connexion à la base de données
const db = new Database(DB_PATH);

// Activer les clés étrangères
db.pragma('foreign_keys = ON');

module.exports = db;

