# Aide de l'IA pour connaitre les fonctions principales et la synthaxe de pandas + pour certains calculs
import pandas as pd

# La fonction principale
def calculer_stats(df):
    """ Appelle toutes les fonctions d'analyse et retourne un dict final"""
    return {
        "repartition_hf": calculer_repartition_hf(df),
        "tranches_age": calculer_tranche_age(df),
        "types_consultation": calculer_type_consultation(df),
        "patients_fidelises": calculer_patients_fidelises(df),
        "consultations_par_mois": calculer_consultations_par_mois(df),
        "consultations_par_jour": calculer_consultations_jours(df),
        "heatmap_heures": calculer_heures_demandees(df)
    }


# Les différentes fonctions indépendantes
def calculer_repartition_hf(df):
    """ Renvoie la répartition H/F avec nombres et pourcentages"""
    counts = df["Civilité"].value_counts()
    total = counts.sum()
    return {
        "nombres": counts.to_dict(),
        "pourcentages": (counts / total * 100).round(1).to_dict()
    }

def calculer_type_consultation(df):
    """ Renvoie le nombre et le pourcentage du type de consultation"""
    counts = df["Motif du RDV"].value_counts()
    total = counts.sum()
    return {
        "nombres": counts.to_dict(),
        "pourcentages": (counts / total * 100).round(1).to_dict()
    }

# Conversion du résultat suite conseil IA en dict python // to_period.size pour garder ordre chronologique
def calculer_consultations_par_mois(df):
    """ Renvoie le nombre de consultations par mois"""
    resultats = df.groupby(df["Date de début"].dt.to_period("M")).size()
    return {str(k): int(v) for k, v in resultats.items()}

# Logique de calcul (nombre_consultations / nombre_jours_distincts) et syntaxe expliquées par IA
def calculer_consultations_jours(df):
    """ Renvoie le nombre moyen de consultations par jour de la semaine"""
    traduction = {
        "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
        "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche"
    }
    ordre = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Ajouter une colonne temporaire "jour de la semaine" et "date sans heure"
    df_temp = df.copy()
    df_temp["jour_semaine"] = df_temp["Date de début"].dt.day_name()
    df_temp["date_seule"] = df_temp["Date de début"].dt.date

    # Total de consultations par jour de la semaine
    total_consultations = df_temp.groupby("jour_semaine").size()

    # Nombre de jours distincts (nombre de lundis, mardis, etc.)
    jours_distincts = df_temp.groupby("jour_semaine")["date_seule"].nunique()

    # Moyenne
    moyennes = (total_consultations / jours_distincts).round(1)

    # Réordonner et traduire
    moyennes = moyennes.reindex(ordre, fill_value=0)
    return {traduction[k]: float(v) for k, v in moyennes.items()}



def calculer_heures_demandees(df):
    """ Preparer les stats pour heatmap des heures les plus demandees"""
    traduction = {
            "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
            "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche"
        }
    ordre = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Ajouter une colonne temporaire "jour de la semaine" et "heure"
    df_temp = df.copy()
    df_temp["jour_semaine"] = df_temp["Date de début"].dt.day_name()
    df_temp["heure"] = df_temp["Date de début"].dt.hour

    # Faire le tableau croisé sous forme agenda
    tableau_croise = pd.crosstab(df_temp["heure"], df_temp["jour_semaine"])

    # Réordonner et traduire
    tableau_croise = tableau_croise.reindex(columns=ordre, fill_value=0)
    tableau_croise = tableau_croise.reindex(index=range(8, 21), fill_value=0)
    return {
        traduction[jour]: {int(heure): int(nombre) for heure, nombre in series.items()}
        for jour, series in tableau_croise.items()
    }


def calculer_patients_fidelises(df):
    """ Connaitre sur l'ensemble des consultations le pourcentage de nouveaux patients et de récurrents"""

    # Trier df par date pour avoir la première consult de chaque patient
    df_chrono = df.sort_values("Date de début")

    # Détecter les patients déja venus
    duplique = df_chrono["Doctolib Patient ID"].duplicated()

    # Resultat et pourcentage
    fideles = duplique.sum()
    nouveaux = len(duplique) - fideles

    total = fideles + nouveaux

    return {
        "nouveaux": {"nombre": int(nouveaux), "pourcentage": round(float((nouveaux*100)/total),1)},
        "fideles": {"nombre": int(fideles), "pourcentage": round(float((fideles*100)/total),1)}
    }



def calculer_tranche_age(df):
    """ Avoir les pourcentages par tranche d'age de la patientele"""

    # Eliminer les doublons de df et ceux sans date de naissance
    df_temp = df.drop_duplicates(subset="Doctolib Patient ID")
    df_temp = df_temp.dropna(subset=["Date de naissance"])

    # Creer colonne age pour chaque patient (IA pour synthaxe et calcul)
    df_temp["age"] = (pd.Timestamp.now() - df_temp["Date de naissance"]).dt.days / 365.25    #.25 pour années bissextiles

    # Créer des classes (IA synthaxe)
    df_temp["tranche"] = pd.cut(
        df_temp["age"],
        bins=[0, 2, 10, 20, 30, 40, 50, 60, 70, 150],
        labels=["0-1", "2-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70+"]
    )

    # Calculs des résultats et pourcentage
    total_tranche = df_temp["tranche"].value_counts().sort_index()

    return {
        "nombres": total_tranche.to_dict(),
        "pourcentages": (total_tranche / total_tranche.sum() * 100).round(1).to_dict()
    }
