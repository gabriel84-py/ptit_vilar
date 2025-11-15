// routes/index.js
const express = require('express');
const router = express.Router();
const { getAllArticles } = require('../services/article_admin');

router.get('/', (req, res) => {
  const articles = getAllArticles();
  res.render('index', { articles });
});

module.exports = router;

