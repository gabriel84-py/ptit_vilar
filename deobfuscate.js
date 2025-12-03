#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

// Usage: node deobfuscate.js input.js output.js
const inputFile = process.argv[2];
const outputFile = process.argv[3];

if (!inputFile || !outputFile) {
  console.error("Usage: node deobfuscate.js input.js output.js");
  process.exit(1);
}

// Lire le fichier JS obfusqué
let code = fs.readFileSync(inputFile, 'utf-8');

// Extraire le tableau _1cb52_1 et la clé _2eb6a_2
const arrayMatch = code.match(/const\s+_1cb52_1\s*=\s*(\[[\s\S]*?\]);/);
const keyMatch = code.match(/const\s+_2eb6a_2\s*=\s*(\d+);/);

if (!arrayMatch || !keyMatch) {
  console.error("Impossible de trouver le tableau ou la clé dans le fichier.");
  process.exit(1);
}

// Évaluer le tableau et la clé
const _1cb52_1 = eval(arrayMatch[1]);
const _2eb6a_2 = parseInt(keyMatch[1], 10);

// Définir la fonction de déchiffrement
const _f44fa_3 = (i) => {
  const a = _1cb52_1[i];
  return String.fromCharCode(...a.map(c => c ^ _2eb6a_2));
};

// Remplacer toutes les occurrences de _f44fa_3(n) par la chaîne déchiffrée
code = code.replace(/_f44fa_3\((\d+)\)/g, (match, p1) => {
  const index = parseInt(p1, 10);
  return JSON.stringify(_f44fa_3(index)); // chaîne en quotes
});

// Écrire le code dé-obfusqué
fs.writeFileSync(outputFile, code, 'utf-8');
console.log(`Fichier dé-obfusqué écrit dans : ${outputFile}`);
