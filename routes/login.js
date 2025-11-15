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

// routes/login.js (version async)
router.post('/check', async (req, res) => {
  try {
    const { email, password } = req.body;
    const ok = await authUser(email, password); // <-- await ici

    if (ok) {
      const token = serializer.dumps({ email, is_admin: true });
      res.cookie('auth', token, { httpOnly: true, maxAge: 24*60*60*1000, path: '/' });
      return res.redirect('/admin');
    } else {
      return res.render('login_error', { email });
    }
  } catch (err) {
    console.error('Login error:', err);
    return res.status(500).send('Erreur serveur');
  }
});


router.get('/logout', (req, res) => {
  res.clearCookie('auth', { path: '/' });
  res.redirect('/login');
});

module.exports = router;

