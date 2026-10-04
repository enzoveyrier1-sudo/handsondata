import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import pandas as pd
from analyses import calculer_stats
from graphiques import graphique_repartition_hf, graphique_tranches_age, graphique_types_consultation, graphique_patients_fidelises, graphique_consultations_mois, graphique_consultations_jours, graphique_heatmap
import json

from aide import apology, login_required

# Configurer l'application et les sessions
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configurer la database
db = SQL("sqlite:///handsondata.db")

# Désactive le cache navigateur pour la sécurité des données affichées (Copie de finance et expliquée par IA)
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Les routes de l'app
@app.route("/")
@login_required
def accueil():
    """Affiche la possibilité d'uploader un csv et les dernieres analyses"""
    historique_5 = db.execute("SELECT * FROM historique WHERE user_id = ? ORDER BY date_analyse DESC LIMIT 5", session["user_id"])

    return render_template("accueil.html", historique_5=historique_5)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Permettre la creation d'un compte"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Nom d'utilisateur requis", 400)
        if not password:
            return apology("Mot de passe requis", 400)
        if password != confirmation:
            return apology("Le mot de passe et sa confirmation doivent êtres identiques", 400)

        hash = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, hash)
        except ValueError:
            return apology("Ce nom d'utilisateur existe déjà", 400)

        return redirect("/login")

    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Connecter l'utilisateur"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("Nom d'utilisateur requis", 400)
        if not password:
            return apology("Mot de passe requis", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Identifiant ou mot de passe incorrect", 400)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """ Deconnecter l'utilisateur"""
    session.clear()
    return redirect("/login")



@app.route("/tutoriel")
def tutoriel():
    """ Donner un court tutoriel à l'utilisateur"""
    return render_template("tutoriel.html")


@app.route("/rgpd")
def rgpd():
    """ Informer l'utilisateur que les données ne sont pas stockées directement et que l'appli est safe"""
    return render_template("rgpd.html")


@app.route("/analyser", methods=["GET", "POST"])
@login_required
def analyser():
    """ Propose d'uploader un CSV, le nettoie et creer une analyse"""
    if request.method == "POST":
        fichier = request.files.get("fichier")

        # Faire toutes les verifications necessaires avant d'analyser
        # Pour la partie manip de fichier + pandas => IA (nom de méthodes, explication des concepts pandas)
        if not fichier or fichier.filename == '':
            return apology("Le fichier est incorrect", 400)
        if not fichier.filename.endswith(".csv"):
            return apology("Le fichier doit être au format CSV", 400)

        # Sauvegarder le fichier et le lire avec pandas
        chemin = os.path.join("uploads", fichier.filename)
        fichier.save(chemin)

        try:
            df = pd.read_csv(chemin, sep=";")
        except Exception:
            return apology("Le fichier est illisible", 400)
        finally:
            # Supprimer le fichier CSV temporaire (règle rgpd) (IA synthaxe)
            try:
                os.remove(chemin)
            except OSError:
                pass


        # Verifier, anonymiser, nettoyer, convertir le fichier (ordre)
        colonnes = ["Motif du RDV",
                    "Civilité",
                    "Date de naissance",
                    "Date de début",
                    "Doctolib Patient ID"]

        for colonne in colonnes:
            if colonne not in df.columns:
                return apology("Le format du CSV est incorrect", 400)

        colonnes_a_supprimer = ["Id", "Agenda", "Notes", "Date de saisie", "Date de dernière mise à jour",
                                    "Créé par", "Statut", "RDV Internet", "Nouveau patient",
                                    "Honoraires CB", "Honoraires Espèces", "Honoraires Chèques",
                                    "Honoraires Tiers payant", "Honoraires Restant à régler",
                                    "Agenda de ressource", "Prénom du patient", "Nom du patient",
                                    "Nom de naissance", "Téléphone portable", "Téléphone secondaire",
                                    "Email du patient", "Adresse", "Code postal", "Ville",
                                    "Heure d'arrivée", "Heure de prise en charge", "Heure de départ",
                                    "Symptômes COVID-19", "Identifiant Externe", "Durée du RDV","Honoraires Total réglé"]
        df = df.drop(columns=colonnes_a_supprimer, errors="ignore")

        # Conversion en date + limite l'analyse aux 3 dernieres annees
        df["Date de début"] = pd.to_datetime(df["Date de début"], errors="coerce")
        df["Date de naissance"] = pd.to_datetime(df["Date de naissance"], errors="coerce")

        # Limiter l'analyse aux 3 dernières années
        date_limite = pd.Timestamp.now() - pd.DateOffset(years=3)
        df = df[df["Date de début"] >= date_limite]


        # Analyses statistiques
        stats = calculer_stats(df)

        # Sauvegarder les données
        nb_consultations = len(df)
        nb_patients_uniques = df["Doctolib Patient ID"].nunique()
        periode_debut = df["Date de début"].min().date()
        periode_fin = df["Date de début"].max().date()
        nom_fichier = fichier.filename

        # Convertir stats en JSON (IA pour interet + synthaxe)
        stats_json = json.dumps(stats)


        # INSERT dans historique + récupérer l'id
        id_analyse = db.execute(
                        "INSERT INTO historique (user_id, nom_fichier, periode_debut, periode_fin, nb_consultations, nb_patients_uniques, revenus_total, stats_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        session["user_id"],
                        nom_fichier,
                        periode_debut,
                        periode_fin,
                        nb_consultations,
                        nb_patients_uniques,
                        None,
                        stats_json
        )

        return redirect(f"/dashboard/{id_analyse}")

    else:
        return redirect("/")


@app.route("/dashboard/<int:analyse_id>")
@login_required
def dashboard(analyse_id):
    rows = db.execute("SELECT * FROM historique WHERE id = ? AND user_id = ?", analyse_id, session["user_id"])
    if len(rows) == 1:
        stats = rows[0]["stats_json"]
        stats = json.loads(stats)
        graph_hf = graphique_repartition_hf(stats["repartition_hf"]["pourcentages"])
        graph_tranches_age = graphique_tranches_age(stats["tranches_age"]["pourcentages"])
        graph_types_consultation = graphique_types_consultation(stats["types_consultation"]["pourcentages"])
        graph_fidelisation = graphique_patients_fidelises(stats["patients_fidelises"])
        graph_frequentation = graphique_consultations_mois(stats["consultations_par_mois"])
        graph_consultation_jours = graphique_consultations_jours(stats["consultations_par_jour"])
        graph_heatmap = graphique_heatmap(stats["heatmap_heures"])
        return render_template("dashboard.html", analyse=rows[0], stats=stats, graph_hf=graph_hf, graph_tranches_age=graph_tranches_age,
                               graph_types_consultation=graph_types_consultation, graph_fidelisation=graph_fidelisation, graph_frequentation=graph_frequentation,
                               graph_consultation_jours=graph_consultation_jours, graph_heatmap=graph_heatmap)
    else:
        return apology("Aucune analyse correspondante", 400)



@app.route("/historique")
@login_required
def historique():
    """Affiche la liste complète des analyses passées"""
    analyses = db.execute(
        "SELECT * FROM historique WHERE user_id = ? ORDER BY date_analyse DESC",
        session["user_id"]
    )
    return render_template("historique.html", analyses=analyses)
