// utils/cookie-signer.js
// Adaptateur pour compatibilité avec itsdangerous.URLSafeSerializer
const crypto = require('crypto');
const { SECRET_KEY } = require('../config');

// URLSafeSerializer compatible avec itsdangerous
class URLSafeSerializer {
  constructor(secretKey) {
    this.secretKey = secretKey;
  }

  dumps(obj) {
    // Sérialiser l'objet en JSON
    const data = JSON.stringify(obj);
    
    // Encoder en base64 URL-safe
    const encoded = Buffer.from(data).toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '');
    
    // Créer un HMAC pour la signature
    const hmac = crypto.createHmac('sha1', this.secretKey);
    hmac.update(encoded);
    const signature = hmac.digest('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '');
    
    // Retourner: signature.encoded
    return `${signature}.${encoded}`;
  }

  loads(token) {
    try {
      const parts = token.split('.');
      if (parts.length !== 2) {
        throw new Error('Invalid token format');
      }
      
      const [signature, encoded] = parts;
      
      // Vérifier la signature
      const hmac = crypto.createHmac('sha1', this.secretKey);
      hmac.update(encoded);
      const expectedSignature = hmac.digest('base64')
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=/g, '');
      
      if (signature !== expectedSignature) {
        throw new Error('Invalid signature');
      }
      
      // Décoder le base64 URL-safe
      let base64 = encoded.replace(/-/g, '+').replace(/_/g, '/');
      // Ajouter le padding si nécessaire
      while (base64.length % 4) {
        base64 += '=';
      }
      
      const data = Buffer.from(base64, 'base64').toString('utf-8');
      return JSON.parse(data);
    } catch (error) {
      throw new Error('BadSignature');
    }
  }
}

const serializer = new URLSafeSerializer(SECRET_KEY);

module.exports = serializer;

