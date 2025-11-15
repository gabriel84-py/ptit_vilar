// routes/articles_manage.js
const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { requireLogin } = require('../middleware/auth');
const {
  getAllArticles,
  getAllArchive,
  getArticle,
  createArticle,
  updateArticle,
  deleteArticle,
  deArchive
} = require('../services/article_admin');

// Toutes les routes nécessitent une authentification
router.use(requireLogin);

// Configuration de multer pour l'upload
const UPLOAD_DIR = path.join(__dirname, '../static/uploads');
if (!fs.existsSync(UPLOAD_DIR)) {
  fs.mkdirSync(UPLOAD_DIR, { recursive: true });
}

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, UPLOAD_DIR);
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  }
});

const upload = multer({ storage });

// ------------------- LISTE DES ARTICLES -------------------
router.get('/', (req, res) => {
  const articles = getAllArticles();
  res.render('admin_articles', { articles });
});

// ------------------- CRÉER UN ARTICLE -------------------
router.get('/create', (req, res) => {
  res.render('create_article');
});

router.post('/create', upload.single('image'), (req, res) => {
  const { title, subtitle, content, category } = req.body;
  const image = req.file;
  
  if (subtitle && subtitle.length > 42) {
    return res.status(400).send('Le sous-titre ne peut pas dépasser 42 caractères.');
  }
  
  let imageUrl = null;
  if (image) {
    imageUrl = `/static/uploads/${image.filename}`;
  }
  
  createArticle(title, subtitle || '', content, category || '', imageUrl);
  res.redirect('/admin/articles');
});

// ------------------- MODIFIER UN ARTICLE -------------------
router.get('/edit/:articleId', (req, res) => {
  const articleId = parseInt(req.params.articleId);
  const article = getArticle(articleId);
  const category = req.query.category || '';
  
  if (!article) {
    return res.status(404).send('Article non trouvé');
  }
  
  const categoriesList = [
    "Vie du lycée", "Science et Progrès", "Culture et Arts",
    "Sport", "Un oeil sur le monde", "Autres", "Orientation"
  ];
  
  res.render('edit_article', {
    article,
    selected_category: category,
    categories: categoriesList
  });
});

router.post('/edit/:articleId', upload.single('image'), (req, res) => {
  const articleId = parseInt(req.params.articleId);
  const { title, subtitle, content, category } = req.body;
  const image = req.file;
  
  const existingArticle = getArticle(articleId);
  let imageUrl = existingArticle?.image_url || null;
  
  if (image && image.filename) {
    imageUrl = `/static/uploads/${image.filename}`;
  }
  
  updateArticle(articleId, title, subtitle || '', content, category || '', imageUrl);
  res.redirect('/admin/articles');
});

// ------------------- SUPPRIMER UN ARTICLE -------------------
router.post('/delete/:articleId', (req, res) => {
  const articleId = parseInt(req.params.articleId);
  deleteArticle(articleId);
  res.redirect('/admin/articles');
});

// ------------------- METTRE UN ARTICLE À LA UNE -------------------
router.post('/feature/:articleId', (req, res) => {
  const articleId = parseInt(req.params.articleId);
  const allArticles = getAllArticles();
  
  allArticles.forEach(art => {
    updateArticle(
      art.id,
      art.title,
      art.subtitle,
      art.content,
      art.category,
      art.image_url,
      art.id === articleId
    );
  });
  
  res.redirect('/admin/articles');
});

// ------------------- LISTE DES ARTICLES ARCHIVÉS -------------------
router.get('/archive', (req, res) => {
  const articles = getAllArchive();
  res.render('archive', { articles });
});

// ------------------- DÉSARCHIVER UN ARTICLE -------------------
router.post('/dearchive/:articleId', (req, res) => {
  const articleId = parseInt(req.params.articleId);
  deArchive(articleId);
  res.redirect('/admin/articles/archive');
});

module.exports = router;

