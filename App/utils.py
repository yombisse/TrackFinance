import sqlite3
def get_dashboard_data():
    conn = sqlite3.connect("trackfinance.db")
    cursor = conn.cursor()

    # Nombre total de membres
    cursor.execute("SELECT COUNT(*) FROM Membres")
    nb_membres = cursor.fetchone()[0]

    # Nombre de prêts
    cursor.execute("SELECT COUNT(*) FROM Transactions WHERE type_operation='pret'")
    nb_prets = cursor.fetchone()[0]

    # Nombre de remboursements
    cursor.execute("SELECT COUNT(*) FROM Transactions WHERE type_operation='remboursement'")
    nb_remboursements = cursor.fetchone()[0]

    # Membres à jour
    cursor.execute("SELECT COUNT(*) FROM Membres WHERE statut='a_jour'")
    nb_ajour = cursor.fetchone()[0]

    # Somme cotisations
    cursor.execute("SELECT COALESCE(SUM(montant),0) FROM Transactions WHERE type_operation='cotisation'")
    total_cotisations = cursor.fetchone()[0]

    # Somme prêts
    cursor.execute("SELECT COALESCE(SUM(montant),0) FROM Transactions WHERE type_operation='pret'")
    total_prets = cursor.fetchone()[0]

    # Somme remboursements
    cursor.execute("SELECT COALESCE(SUM(montant),0) FROM Transactions WHERE type_operation='remboursement'")
    total_remboursements = cursor.fetchone()[0]
    total_remboursements+=total_remboursements*0.1

    # Bénéfice = remboursements - prêts
    benefice = total_remboursements - total_prets

    conn.close()

    return {
        "nb_membres": nb_membres,
        "nb_prets": nb_prets,
        "nb_remboursements": nb_remboursements,
        "nb_ajour": nb_ajour,
        "total_cotisations": total_cotisations,
        "total_prets": total_prets,
        "total_remboursements": total_remboursements,
        "benefice": benefice
    }
    # def clearselector(self):
    #     self.dashboard_selector.config(bg="#ffffff")
    #     self.membres_selector.config(bg="#ffffff")
    #     self.transaction_selector.config(bg="#ffffff")
    #     self.pret_selector.config(bg="#ffffff")
    #     self.parametre_selector.config(bg="#ffffff")


    # def selector(self, lb, page):
    #     self.clearselector()
    #     lb.config(bg="#7aaad1")
    #     page()

    # def home_selector(self):
    #     self.clearselector()
    #     self.dashboard_selector.config(bg="#7aaad1")

    # def set_placeholder(self, entry, placeholder):
    #     entry.insert(0, placeholder)
    #     entry.config(foreground="grey")

    #     def on_focus_in(event):
    #         if entry.get() == placeholder:
    #             entry.delete(0, END)
    #             entry.config(foreground="black")

    #     def on_focus_out(event):
    #         if entry.get() == "":
    #             entry.insert(0, placeholder)
    #             entry.config(foreground="grey")

    #     entry.bind("<FocusIn>", on_focus_in)
    #     entry.bind("<FocusOut>", on_focus_out)

    # def statut_value(self, event):
    #     print("Choix du statut :", self.statut_var.get())