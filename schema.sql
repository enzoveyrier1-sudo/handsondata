CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE historique (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date_analyse DATETIME DEFAULT CURRENT_TIMESTAMP,
    nom_fichier TEXT,
    periode_debut DATE,
    periode_fin DATE,
    nb_consultations INTEGER,
    nb_patients_uniques INTEGER,
    revenus_total NUMERIC,
    stats_json TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE INDEX idx_historique_user ON historique(user_id);
