// services/article_admin.js
const Article = require('../models/Article');

function getAllArticles() {
  return Article.findAll(false);
}

function getAllArchive() {
  return Article.findArchived();
}

function getArticle(articleId) {
  return Article.findById(articleId);
}

function createArticle(title, subtitle, content, category, imageUrl) {
  return Article.create(title, subtitle, content, category, imageUrl);
}

function updateArticle(articleId, title, subtitle, content, category, imageUrl, featured = null) {
  return Article.update(articleId, title, subtitle, content, category, imageUrl, featured);
}

function deleteArticle(articleId) {
  return Article.archive(articleId);
}

function deArchive(articleId) {
  return Article.dearchive(articleId);
}

module.exports = {
  getAllArticles,
  getAllArchive,
  getArticle,
  createArticle,
  updateArticle,
  deleteArticle,
  deArchive
};

