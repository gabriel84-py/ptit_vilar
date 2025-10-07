from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from services.auth_user import auth_user
from services.user_exist import user_exist
from services.create_user import create_user

router = APIRouter(prefix="/admin", tags=["Auth"])

@router.get("/", response_class=HTMLResponse)
def dashborad():
    return """"
     <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard</title>
            <style>
                body { font-family: sans-serif; text-align: center; margin-top: 100px; }
                h1 { color: green; }
            </style>
        </head>
        <body>
            <h1>Bienvenue sur ton dashboard !</h1>
            <p>Connexion réussie.</p>
            <a href="/create_user">Créer un utilisateur</a>
        </body>
        </html>
    """


@router.get("/create_user", response_class=HTMLResponse)
def create_user_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Connexion</title>
        <style>
            body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; margin-top: 100px; }
            form { display: flex; flex-direction: column; width: 300px; gap: 10px; }
            input, button { padding: 10px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>Créer un nouvel utilisateur :</h1>
        <form action="/admin/endpoint_create_user" method="get">
            <input type="email" name="email" placeholder="Email" required />
            <input type="password" name="password" placeholder="Mot de passe" required />
            <input type="text" name="is_admin" placeholder="aurat-il les privilèges d'admin : True/False"/>
            <button type="submit">Créer</button>
        </form>
    </body>
    </html>
    """


@router.get("/endpoint_create_user", response_class=HTMLResponse)
def process_login(email: str, password: str, is_admin: bool):
    if user_exist(email):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard</title>
            <style>
                body { font-family: sans-serif; text-align: center; margin-top: 100px; }
                h1 { color: green; }
            </style>
        </head>
        <body>
            <h1>Utilisateur déjà existant</h1>
            <a href="/admin">Retour a ton dashboard</a>
        </body>
        </html>
        """
    else:
        create_user(email=email, passwd=password, admin=is_admin)
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Erreur</title>
            <style>
                body { font-family: sans-serif; text-align: center; margin-top: 100px; }
                h1 { color: red; }
            </style>
        </head>
        <body>
            <h1>Utilisateur créé</h1>
            <p>Parfait !</p>
            <a href="/admin">↩ Retour au dashboard</a>
        </body>
        </html>
        """
