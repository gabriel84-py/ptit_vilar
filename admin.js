// routes/admin.js
const express = require('express');
const router = express.Router();
const { requireLogin } = require('../middleware/auth');
const { getTotalVisitors } = require('../services/visitor_service');
const { getAllUsers } = require('../services/view_users');
const deleteUser = require('../services/delete_user');
const userExist = require('../services/user_exist');
const createUser = require('../services/create_user');

// Toutes les routes admin nécessitent une authentification
router.use(requireLogin);

// ------------------- ADMIN DASHBOARD -------------------
router.get('/', (req, res) => {
  const totalVisitors = getTotalVisitors();
  res.render('admin_dashboard', { total_visitors: totalVisitors });
});

// ------------------- CREATE USER -------------------
router.get('/create_user', (req, res) => {
  res.render('create_user');
});

router.get('/endpoint_create_user', (req, res) => {
  const { email, password } = req.query;
  
  if (userExist(email)) {
    return res.render('user_created', {
      message: "Utilisateur déjà existant",
      success: false
    });
  }
  
  createUser(email, password);
  res.render('user_created', {
    message: "Utilisateur créé avec succès",
    success: true
  });
});

// ------------------- DELETE USER -------------------
router.get('/delete_user', (req, res) => {
  res.render('delete_user');
});

router.get('/endpoint_delete_user', (req, res) => {
  const { email } = req.query;
  
  if (!userExist(email)) {
    return res.render('user_created', {
      message: "Utilisateur n'existe pas",
      success: false
    });
  }
  
  deleteUser(email);
  res.render('user_created', {
    message: "Utilisateur supprimé avec succès",
    success: true
  });
});

router.get('/users', (req, res) => {
  const users = getAllUsers();
  res.render('view_users', { users });
});

module.exports = router;

