# Application Node.js - Journal du lycée

Cette application a été migrée de FastAPI (Python) vers Node.js/Express.

## Installation

Les dépendances sont déjà installées. Si vous devez les réinstaller :

```bash
npm install
```

## Démarrage

Pour démarrer le serveur :

```bash
npm start
```

Ou en mode développement avec rechargement automatique :

```bash
npm run dev
```

Le serveur démarre sur le port 3000 par défaut (ou le port défini dans la variable d'environnement PORT).

## Structure

- `server.js` - Point d'entrée principal de l'application
- `models/` - Modèles de données (User, Article, Visitor)
- `routes/` - Routes de l'application
- `services/` - Logique métier
- `middleware/` - Middlewares Express
- `templates/` - Templates Nunjucks (compatible Jinja2)
- `static/` - Fichiers statiques (CSS, images, etc.)
- `data/app.db` - Base de données SQLite (conservée intacte)

## Base de données

La base de données SQLite existante (`data/app.db`) est conservée et utilisée telle quelle. Toutes les données sont préservées.

## Authentification

L'authentification utilise des cookies signés compatibles avec l'ancien système Python (itsdangerous).

## Notes

- Les templates utilisent Nunjucks qui est compatible avec la syntaxe Jinja2
- La base de données SQLite est la même que celle utilisée par l'application Python
- Toutes les fonctionnalités de l'application Python sont préservées

