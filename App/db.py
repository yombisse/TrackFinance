import sqlite3

def createdb():
    conn = sqlite3.connect('trackfinance.db', timeout=5)
    conn.execute("PRAGMA journal_mode=WAL;")  # Active WAL pour éviter les verrous
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Membres(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        identifiant TEXT UNIQUE NOT NULL,         
        type_identifiant TEXT NOT NULL,           
        name TEXT NOT NULL,
        firstname TEXT NOT NULL,
        date DATETIME,
        adress TEXT NOT NULL,
        contact TEXT NOT NULL,
        statut TEXT CHECK (statut IN ("a_jour", "en_retard", "en_pret")) NOT NULL
    )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pret_id INTEGER,
            membre_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            montant REAL NOT NULL,
            description TEXT NOT NULL,
            type_operation TEXT CHECK(type_operation IN ("cotisation", "pret", "remboursement")) NOT NULL,
            mois TEXT CHECK(mois IN ("Janvier", "Fevrier", "Mars","Avril", "Mai", "Juin","Juillet", "Aout", "Septembre","Octobre", "Novembre", "Decembre")) NOT NULL,
            user_id INTEGER, 
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(membre_id) REFERENCES Membres(id),
            FOREIGN KEY(pret_id) REFERENCES Prets(id),
            CHECK (
                (type_operation IN ('cotisation', 'pret') AND pret_id IS NULL)
                OR
                (type_operation = 'remboursement' AND pret_id IS NOT NULL)
            )
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Prets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER NOT NULL,
            delai INTEGER NOT NULL,
            taux_interet REAL NOT NULL,
            montant_restant REAL NOT NULL,
            user_id INTEGER, 
            FOREIGN KEY(user_id) REFERENCES users(id)
            FOREIGN KEY(transaction_id) REFERENCES Transactions(id)
        )
    ''')

 # Table HistoriqueMembre
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HistoriqueMembre(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            description TEXT,
            date TEXT
        )
        ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            firstname TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')

    conn.commit()
    conn.close()
    conn = sqlite3.connect('trackfinance.db')
    print("Connexion OK")
    conn.close()
