// routes/articles.js
const express = require('express');
const router = express.Router();
const { getArticle } = require('../services/article_admin');
const Article = require('../models/Article');
const { marked } = require('marked');

// Configuration de marked pour les extensions
marked.setOptions({
  breaks: true,
  gfm: true
});

router.get('/:articleId', (req, res) => {
  const articleId = parseInt(req.params.articleId);
  const article = getArticle(articleId);
  
  if (!article) {
    return res.status(404).send('<h1>Article introuvable</h1>');
  }
  
  // Convertir le contenu Markdown en HTML
  const htmlContent = marked(article.content);
  
  res.render('article_detail', { article, html_content: htmlContent });
});

module.exports = router;

