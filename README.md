# HandsOnData
#### Video Demo: https://youtu.be/mTqumSaPNz4
#### Description:

## Présentation de HandsOnData
La pratique d'une discipline en libéral se rapproche de celle d'un auto-entrepreneur, et pour qu'une activité fonctionne, elle doit être comprise. Les ostéopathes disposent pourtant de toutes les données nécessaires via leur agenda Doctolib, mais d'aucun outil simple pour les exploiter. C'est l'objectif de HandsOnData.

Je suis Enzo Veyrier, ostéopathe D.O. Lors de mes études d'ostéopathie j'ai fait un mémoire dans lequel j'ai analysé des données de santé pour comprendre le diagnostic ostéopathique. C'est suite à mon mémoire que j'ai décidé d'utiliser l'analyse de données pour contribuer au développement de la profession d'ostéopathe.  HandsOnData est une app web pour les ostéopathes. Elle permet à l'utilisateur d'analyser des données du cabinet et d'en faire des statistiques depuis un export "Historique de RDV" de Doctolib afin de comprendre son activité.

## Parcours utilisateur
1. Créer un compte puis se connecter
2. Depuis la page d'accueil, importer son export Doctolib
3. Cliquer sur "Analyser" pour lancer l'analyse de données, redirection vers la page "Dashboard" avec visualisation des statistiques
4. Possibilité de voir l'historique de ses anciennes analyses
5. Possibilité de lire un tutoriel sur l'exportation du fichier depuis Doctolib
6. Possibilité de lire une notice sur les règles RGPD mises en place par HandsOnData
7. Déconnexion

Chaque analyse est enregistrée et peut être visualiser à tout moment sans ré-importer le fichier.

## Les analyses
1. Répartition H/F : la proportion d'hommes et de femmes parmi les patients (camembert).
Permet de comprendre les données démographiques de son cabinet. Une forte proportion de femmes peut induire des formations dans des problématiques de grossesse, de ménopause, etc...
2. Tranches d'âge : la répartition des patients par tranche d'âge, des nourrissons aux plus de 70 ans (barres).
Permet de cibler et se former en fonction des patients qui viennent, une forte proportion de nourrissons peut induire la formation en pédiatrie tandis qu'une forte proportion de séniors peut induire des formations en gériatrie.
3. Types de consultation : la part de chaque motif de RDV (première consultation, suivi, nourrisson, sportif…) (barres horizontales).
Comprendre les motifs de rendez-vous peut par exemple pousser à se former dans le sport si beaucoup de sportifs viennent au cabinet, changer les motifs les moins pris sur doctolib pour en ajouter des nouveaux plus axés sur d'autres populations.
4. Origine des consultations : la part des consultations qui sont des premières visites, contre des visites de retour (camembert).
Comprendre la répartition de patients nouveaux et fidèles peut donner des idées sur la stratégie du cabinet. Peu de nouveaux patients peut pousser à chercher de nouvelles acquisitions ou à l'inverse peu de fidèles peut inciter à mettre en place des aides pour fidéliser le patient.
5. Évolution mensuelle : le nombre de consultations par mois sur les 3 dernières années (courbe).
Avoir une courbe de visualisation dans le temps permet de comprendre la tendance générale du cabinet, si au moment de l'analyse, le cabinet se développe ou non, ces données peuvent être croisées avec d'anciennes analyses pour voir si des différences existent et les raisons potentielles. Permet aussi de comprendre les périodes de l'année les plus chargées et les périodes les plus calmes.
6. Moyenne par jour de la semaine : le nombre moyen de consultations pour chaque jour travaillé (barres).
À plus petite échelle comprendre quels jours de la semaine sont les plus demandés permet d'agir directement sur son emploi du temps. Un jeune ostéopathe a tendance à ouvrir tous les jours en début d'activité pour se développer. Mais au moment de calmer son rythme, ce type d'analyse permet de faire un choix stratégique et éclairé.
7. Créneaux les plus demandés : une heatmap heures × jours, au format agenda.
Tout comme les jours de la semaine, comprendre les heures où le cabinet attire du monde permet de gérer son emploi du temps de la meilleure des façons. En connaissant ses heures les plus demandées et celles les plus calmes, un ostéopathe peut planifier des RDV personnels sans l'appréhension d'une perte de chiffre la semaine concernée.


## Les fichiers
### app.py
Le fichier principal, qui contient toutes les routes de l'app web :
- /register pour la création d'un compte, le hashage du mot de passe.
- /login pour la connexion d'un utilisateur.
- /logout pour la déconnexion.
- /tutoriel permet à n'importe qui de lire un tutoriel sur l'exportation du fichier depuis Doctolib.
- /rgpd permet à n'importe qui de lire la façon dont l'app web gère les données, les précautions qui sont prises.
- / est la page d'accueil, permet à l'utilisateur d'uploader un fichier, de l'analyser ou de voir ses 5 dernières analyses.
- /analyser propose d'uploader un fichier, le fichier est enregistré temporairement sur le serveur, lu et mis dans un dataframe temporaire avec pandas puis supprimé directement (même si erreur de lecture). Le dataframe est ensuite nettoyé (suppression de toutes les données sensibles, noms, prénoms et des données inutiles aux analyses), certaines données sont converties et celles supérieures à 3 ans sont supprimées (limitation de l'analyse aux trois dernières années pour avoir une tendance récente). Elle lance les statistiques et sauvegarde les résultats des analyses. Les statistiques sont converties en json pour être stockées dans une database avec les analyses liées à l'utilisateur connecté. Une fois l'analyse terminée, elle redirige vers /dashboard avec l'id de l'analyse actuelle.
- /dashboard récupère l'id d'une analyse, vérifie que l'analyse appartient bien à l'utilisateur connecté, convertit les stats.JSON en dict puis appelle les fonctions pour la création de graphique.
- /historique affiche la liste complète des analyses de l'utilisateur connecté, avec un lien vers chaque dashboard.
Il joue le rôle de "controller" de l'architecture MVC. Elle redirige vers les différentes routes, en fonction des demandes de l'utilisateur.

### aide.py
Contient des fonctions utiles sur différents routes de app.py :
- login_required : le décorateur inspiré du pset finance, pour sécuriser l'accès à certaines routes (/logout, /analyser, /dashboard, /historique).
- Apology : retourne un message d'erreur adapté si certaines fonctionnalités rencontrent un problème.

### analyses.py
Le fichier qui contient toutes les analyses statistiques :
- calculer_stats : appelle toutes les autres fonctions d'analyses et renvoie un dictionnaire global.
- calculer_repartition_hf : calcule la répartition d'homme et de femme présents dans l'analyse.
- calculer_tranche_age : Calcule la répartition des tranches d'âge dans l'analyse.
- calculer_type_consultation : Calcule les motifs de consultations les plus fréquents.
- calculer_patients_fidelises : Calcule le nombre de consultation avec des patients nouveaux et récurrents dans l'analyse.
- calculer_consultations_par_mois : Calcule le nombre de consultations sur les 36 derniers mois.
- calculer_consultations_jours : Calcule le nombre moyen de consultations par jours de la semaine.
- calculer_heures_demandees : Calcule le nombre de consultations pour chaque créneau jour x heure.

### graphiques.py
Le fichier qui construit les graphiques via matplotlib (camembert, barchart et barchart horizontal, courbe, heatmap). Convertit les figures en base64 pour le template dashboard.html.

### templates
Un layout pour le style global et la présentation inspiré du pset finance. Avec une navbar.
Des templates :
- accueil.html affiche les possibilités d'uploader le fichier ou de voir ses anciennes analyses.
- apology.html : affiche les messages d'erreur.
- dashboard.html : reçoit images encodées en texte, affiche les graphiques à l'utilisateur.
- historique.html : Affiche les analyses anciennes de l'utilisateur.
- login.html : inspiré du pset finance, permet la connexion de l'utilisateur.
- register.html : permet la création de compte.
- rgpd.html : affiche le message d'information relatif à la gestion des données sensibles.
- tutoriel.html : affiche un tutoriel sur l'exportation du fichier sur Doctolib.


### database
handsondata.db est la database du projet. Elle contient 2 tables :
- users : avec identifiants et hash du mot de passe.
- historique : contient toutes les analyses d'un utilisateur (via son user_id). Contient les métadonnées (nom du fichier, période, etc...), les statistiques agrégées en JSON, aucune données patients.


## Les choix de conception
Dans le cadre du projet HandsOnData, certains choix ont été faits :
- Certaines statistiques retirées des analyses, par exemple les revenus moyens du cabinet (car les ostéopathes utilisent souvent un logiciel tiers qui gère déjà leur comptabilité et n'utilisent donc pas Doctolib pour cela), le taux d'annulation (car bien qu'intéressante, cette statistique ne donne pas d'informations sur les raisons des annulations et donc peu de levier pour y remédier).
- Les analyses sont limitées aux trois dernières années, en effet, des statistiques sur un plus long terme ne reflètent plus la tendance récente d'un cabinet mais une évolution sur le long terme. Cela aurait pu être un choix, mais je considère que le court terme pour ce type d'analyse est plus important.
- Le stockage dans la table "historique" comprend des métadonnées pour avoir les principales informations de chaque analyse (période analysée, nom du fichier, nombre de consultations analysées), cette colonne permet d'afficher la liste des anciennes analyses. La dernière colonne contient les résultats statistiques uniquement en format JSON qui permet de recréer le dashboard propre à cette analyse a posteriori.
- Les graphiques en base64 plutôt qu'en fichiers images. Une première approche aurait consisté à enregistrer chaque graphique en PNG dans le dossier static/. Mais ces fichiers se seraient accumulés sur le serveur à chaque analyse, et tout fichier de static/ est accessible publiquement à qui connaît son adresse : un utilisateur aurait pu consulter les graphiques d'un autre. J'ai donc choisi de générer les graphiques en mémoire, à chaque affichage du dashboard, à partir des statistiques stockées en base. Chaque image est convertie en texte (base64) et insérée directement dans la page HTML. Aucune image n'est écrite sur le disque, et un graphique n'est visible que par l'utilisateur propriétaire de l'analyse.
- Une première version laissait le CSV sur le serveur si la lecture échouait, ce potentielle problème a été repéré lors d'une discussion avec un lead dev. Le bloc finally garantit sa suppression dès la fin de la lecture, qu'elle réussisse ou non.


## Limites et améliorations
### Limites
Le projet comporte des limites, en voici quelques-unes :
- La pseudonymisation des données, les données ne sont pas totalement anonymisées, des techniques d'anonymisation plus sophistiquées mériteraient d'être mises en place.
- Le projet dépend du format Doctolib, si le format du fichier d'exportation change, alors le projet ne fonctionne plus et doit être remis à jour en fonction. De plus un ostéopathe n'utilisant pas Doctolib mais un autre logiciel d'agenda ne peut utiliser les services de HandsOnData.
- Le test a été fait via des données fictives, pas sur un véritable export Doctolib.

### Pistes d'évolution
Certaines fonctionnalités mériteraient d'être améliorées :
- Ajout de nouvelles statistiques via un fichier comptable par exemple pour une analyse financière plus poussée.
- Croisement des données dans des analyses multivariées pour comprendre et prédire plus qu'une simple analyse "Compte rendu".
- Améliorations de l'expérience utilisateur via les couleurs, l'interactivité, etc...
- Ajout de la possibilité de s'adapter à d'autres fichiers (excel, agenda hors Doctolib, etc...).
- Possibilité de comparer directement sur l'application une nouvelle analyse avec une ancienne pour voir l'évolution du cabinet.
- Sécurisation renforcée des données, techniques d'anonymisation sophistiquées.

## Installation
1. Installer les dépendances : `pip install -r requirements.txt`
2. Un export fictif est fourni dans exemple/test_doctolib_complet.csv pour tester l'application sans compte Doctolib.
3. Vérifier la présence du dossier `uploads/` (sinon : `mkdir uploads`) et de la base `handsondata.db`
4. Lancer l'application : `flask run`
5. Créer un compte, puis importer un export « Historique de RDV » de Doctolib depuis la page d'accueil


## Utilisation de l'IA
Conformément aux règles du projet final CS50, j'ai utilisé l'IA comme tuteur et assistant sur certaines fonctionnalités du projet. Les parties où elle à eu un rôle sont liées à la compréhension et à la synthaxe de pandas, matplotlib (aide dans le code de certaines statistiques et  la conversion des graphiques en base64). La grille du dashboard a été ajouté par IA (au départ une première version codée par moi, puis amélioration pour le rendu visuel de cette dernière). Le fichier exemple est entièrement généré aléatoirement par IA et ne contient que des données aléatoires.
