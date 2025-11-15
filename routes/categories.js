// routes/categories.js
const express = require('express');
const router = express.Router();
const { getAllArticles } = require('../services/article_admin');

router.get('/', (req, res) => {
  const category = req.query.category || '';
  const search = req.query.search || '';
  
  let allArticles = getAllArticles();
  
  // Filtrage par catégorie
  if (category) {
    allArticles = allArticles.filter(a => a.category === category);
  }
  
  // Filtrage par recherche
  if (search) {
    const searchLower = search.toLowerCase();
    allArticles = allArticles.filter(a => 
      a.title?.toLowerCase().includes(searchLower) || 
      a.subtitle?.toLowerCase().includes(searchLower)
    );
  }
  
  const categoriesList = [
    "Vie du lycée", "Science et Progrès", "Culture et Arts",
    "Sport", "Un oeil sur le monde", "Autres", "Orientation"
  ];
  
  res.render('categories', {
    articles: allArticles,
    categories: categoriesList,
    selected_category: category,
    search
  });
});

module.exports = router;

