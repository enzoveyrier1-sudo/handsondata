# Conversion figure -> base64 : code de "plomberie" fourni par IA
import io
import base64
import matplotlib

matplotlib.use("Agg")   # mode sans écran, obligatoire sur un serveur
import matplotlib.pyplot as plt

# Style commun des graphiques (couleurs de l'identité HandsOnData)
plt.rcParams.update({
    "axes.prop_cycle": matplotlib.cycler(color=["#2A9D8F", "#FF8C61", "#14283F", "#8FD3CA", "#F4C7B3", "#5B6B7A"]),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#C5CED6",
    "axes.labelcolor": "#5B6B7A",
    "xtick.color": "#5B6B7A",
    "ytick.color": "#5B6B7A",
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.titlecolor": "#14283F",
    "axes.titlepad": 12,
})

def figure_en_base64(fig):
    """Convertit une figure Matplotlib en chaîne base64 pour le HTML"""
    buffer = io.BytesIO()                      # faux fichier en mémoire
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)                             # libère la mémoire
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# Cette partie codé par moi même => Aide de l'IA sur concept matplotlib, synthaxe
def graphique_repartition_hf(pourcentages):
    fig, ax = plt.subplots()     # crée une figure et une zone de dessin

    # ax.TYPE_DE_GRAPHIQUE()    # dessine : bar, pie, plot...
    ax.pie(list(pourcentages.values()), labels=list(pourcentages.keys()), autopct="%1.1f%%")

    ax.set_title("Répartition H/F")          # titre
    return figure_en_base64(fig)


def graphique_tranches_age(pourcentages):
    fig, ax = plt.subplots()

    ax.bar(list(pourcentages.keys()), list(pourcentages.values()))

    ax.set_title("Tranches d'âge des patients")
    ax.set_xlabel("Tranches d'âge")
    ax.set_ylabel("Pourcentage %")
    return figure_en_base64(fig)



def graphique_types_consultation(pourcentages):
    fig, ax = plt.subplots()

    ax.barh(list(pourcentages.keys()), list(pourcentages.values()))

    ax.set_title("Types de consultation")
    ax.set_xlabel("Pourcentage %")
    ax.set_ylabel("Types de consultation")
    return figure_en_base64(fig)



def graphique_patients_fidelises(fidelisation):
    fig, ax = plt.subplots()

    valeurs = [fidelisation["nouveaux"]["pourcentage"], fidelisation["fideles"]["pourcentage"]]
    etiquettes = ["Premières consultations", "Consultations de suivi"]
    ax.pie(valeurs, labels=etiquettes, autopct="%1.1f%%")

    ax.set_title("Origine des consultations")
    return figure_en_base64(fig)



def graphique_consultations_mois(nombre):
    mois = list(nombre.keys())
    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(mois, list(nombre.values()), marker="o")

    ax.set_xticks(range(0, len(mois), 3))
    ax.set_xticklabels(mois[::3], rotation=45)
    ax.set_title("Évolution de la fréquentation du cabinet")
    ax.set_xlabel("Période")
    ax.set_ylabel("Nombre de consultations")
    return figure_en_base64(fig)



def graphique_consultations_jours(moyenne):
    fig, ax = plt.subplots()

    ax.bar(list(moyenne.keys()), list(moyenne.values()))

    ax.set_title("Moyenne de consultations par jour")
    ax.set_xlabel("Jours de la semaine")
    ax.set_ylabel("Moyenne de consultations")
    return figure_en_base64(fig)


# Heatmap : aide IA (construction matrice / synthaxe matplotlib)
def graphique_heatmap(heatmap):
    jours = list(heatmap.keys())
    heures = list(heatmap["Lundi"].keys())

    # Réorganiser les données : une ligne par heure, une colonne par jour
    matrice = []
    for heure in heures:
        ligne = []
        for jour in jours:
            ligne.append(heatmap[jour][heure])
        matrice.append(ligne)

    fig, ax = plt.subplots()
    palette = matplotlib.colors.LinearSegmentedColormap.from_list("hod", ["#F3F6F8", "#2A9D8F", "#14283F"])
    image = ax.imshow(matrice, cmap=palette, aspect="auto")

    # Étiquettes des axes : jours en haut, heures à gauche
    ax.set_xticks(range(len(jours)))
    ax.set_xticklabels([jour[:3] for jour in jours])
    ax.set_yticks(range(len(heures)))
    ax.set_yticklabels([f"{h}h" for h in heures])

    fig.colorbar(image, ax=ax, label="Nombre de consultations")
    ax.set_title("Créneaux les plus demandés")
    return figure_en_base64(fig)
