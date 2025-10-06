from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from services.auth_user import auth_user

router = APIRouter(prefix="/login", tags=["Auth"])


@router.get("/", response_class=HTMLResponse)
def show_login_form():
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
        <h1>Se connecter</h1>
        <form action="/login/login" method="get">
            <input type="email" name="email" placeholder="Email" required />
            <input type="password" name="password" placeholder="Mot de passe" required />
            <button type="submit">Connexion</button>
        </form>
    </body>
    </html>
    """


@router.get("/login", response_class=HTMLResponse)
def process_login(email: str, password: str):
    if auth_user(email, password):
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
            <h1>Bienvenue sur ton dashboard !</h1>
            <p>Connexion réussie.</p>
            <p></p>
        </body>
        </html>
        """
    else:
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
            <h1>Échec de la connexion</h1>
            <p>Vérifie ton email ou ton mot de passe.</p>
            <a href="/auth">↩ Retour</a>
        </body>
        </html>
        """
