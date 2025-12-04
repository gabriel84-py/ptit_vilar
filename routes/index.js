// routes/index.js
const express = require('express');
const router = express.Router();
const { getAllArticles } = require('../services/article_admin');

router.get('/', (req, res) => {
  const articles = getAllArticles().slice().reverse();
  const featuredArticle = articles.find(a => a.featured === true);
  res.render('index', { articles, featuredArticle });
});


module.exports = router;

