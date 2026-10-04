from flask import redirect, render_template, session

# Nécessaire pour préserver le nom des fonctions décorées (utilisé par @login_required et expliquée par IA)
from functools import wraps


# Les fonctions pour certaines associées d'une docstring (explique la fonction)

# Décorateur copié depuis finance qui permet de vérifier sur les routes concernées qu'un utilisateur et connecté sinon renvoie vers la page de connexion
def login_required(f):
    """Décorateur qui redirige vers /login si l'utilisateur n'est pas connecté."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function



def apology(message, code=400):
    """Affiche une page d'erreur avec un message pour l'utilisateur"""
    return render_template("apology.html", code=code, message=message), code
