// routes/formation_md.js
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.render('formation_md');
});

module.exports = router;

