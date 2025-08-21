# finance_utils.py
import sqlite3

DB_PATH = 'trackfinance.db'

# -------------------------------
# Seuils configurables
# -------------------------------
SEUIL_SOLDE = 1000  # Solde disponible minimum
SEUIL_PRET = 5000   # Prêts en cours maximum

# -------------------------------
# Fonctions génériques
# -------------------------------
def get_total(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0

# -------------------------------
# Totaux principaux
# -------------------------------
def get_total_cotisations():
    return get_total("SELECT SUM(montant) FROM Transactions WHERE type_operation='cotisation'")

def get_total_prets():
    return get_total("SELECT SUM(montant) FROM Transactions WHERE type_operation='pret'")

def get_total_remboursements():
    return get_total("SELECT SUM(montant) FROM Transactions WHERE type_operation='remboursement'")

def get_prets_en_cours():
    return get_total_prets() - get_total_remboursements()

def nb_membres():
    return get_total("SELECT COUNT(*) FROM Membres")

def nb_prets_en_cours():
    return get_total("SELECT COUNT(*) FROM Prets WHERE montant_restant > 0")

# -------------------------------
# Calculs avancés
# -------------------------------
def solde_principal():
    return get_total_cotisations() + get_total_remboursements() - get_total_prets()

def solde_disponible():
    return solde_principal() - get_prets_en_cours()

def ratio_pret_cotisation():
    cotisations = get_total_cotisations()
    prets_en_cours = get_prets_en_cours()
    return round(prets_en_cours / cotisations, 2) if cotisations != 0 else 0

# -------------------------------
# Notifications / alertes
# -------------------------------
def get_alertes():
    alertes = []
    solde = solde_disponible()
    prets = get_prets_en_cours()

    if solde < SEUIL_SOLDE:
        alertes.append(f"⚠️ Solde disponible faible : {solde} < {SEUIL_SOLDE}")

    if prets > SEUIL_PRET:
        alertes.append(f"⚠️ Prêts en cours élevés : {prets} > {SEUIL_PRET}")

    if ratio_pret_cotisation() > 0.5:
        alertes.append(f"⚠️ Ratio prêt/cotisation élevé : {ratio_pret_cotisation()*100}%")

    return alertes
