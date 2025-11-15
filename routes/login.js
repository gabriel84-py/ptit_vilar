// routes/login.js
const express = require('express');
const router = express.Router();
const authUser = require('../services/auth_user');
const serializer = require('../utils/cookie-signer');
const { getAllArticles } = require('../services/article_admin');

// Page de connexion
router.get('/', (req, res) => {
  const articles = getAllArticles();
  res.render('login', { articles });
});

// Vérification du login
router.post('/check', (req, res) => {
  const { email, password } = req.body;
  
  if (authUser(email, password)) {
    // Génère un token signé (équivalent à itsdangerous)
    const token = serializer.dumps({ email, is_admin: true });
    
    res.cookie('auth', token, {
      httpOnly: true,
      maxAge: 60 * 60 * 24 * 1000, // 24 heures
      path: '/'
    });
    
    res.redirect('/admin');
  } else {
    res.render('login_error', { email });
  }
});

router.get('/logout', (req, res) => {
  res.clearCookie('auth', { path: '/' });
  res.redirect('/login');
});

module.exports = router;

