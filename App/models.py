import sqlite3

import tkinter as tk
from tkinter import messagebox
from tkinter import *


db_name = 'trackfinance.db'
class Membre:
    db_name = "trackfinance.db"

    @staticmethod
    def ajouter_membre(identifiant,type_identifiant,name, firstname, date, adress, contact, statut):
        conn = None
        try:
            conn = sqlite3.connect(Membre.db_name, timeout=5)
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO Membres(identifiant,type_identifiant,name, firstname, date, adress, contact, statut)
                VALUES (?, ?, ?, ?, ?, ?,?,?)
                ''',
                (identifiant,type_identifiant,name, firstname, date, adress, contact, statut)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except sqlite3.OperationalError as e:
            print("Erreur SQLite :", e)
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
#Affichage
    def show_members():
        try:
            conn=sqlite3.connect('trackfinance.db')
            cursor=conn.cursor()
            cursor.execute(
                '''SELECT * FROM Membres'''
            )
            conn.commit()
            membres=cursor.fetchall()
            return membres
        except sqlite3.OperationalError as e:
            messagebox.showerror("Erreur de connexion a la base de donnee:",e)
            return False
        finally:
            if conn:
                conn.close()


    @staticmethod
    def get_all_names():
        conn = None
        try:
            conn = sqlite3.connect(Membre.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT name,firstname FROM Membres")
            result = cursor.fetchall()
            return result
        except sqlite3.OperationalError as e:
            messagebox.showerror("Erreur SQL", str(e))
            return []
        finally:
            if conn:
                conn.close() 

    def log_membre_action(membre_id, action, description):
        conn = sqlite3.connect("trackfinance.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO HistoriqueMembre (membre_id, action, description, date)
            VALUES (?, ?, ?, date('now'))
        """, (membre_id, action, description))
        conn.commit()
        conn.close()

                
    
class Transactions:
    @staticmethod
    def effectuer_transaction(membre_id, montant, date, description, type_operation,mois, pret_id=None):
        """
        Ajoute une transaction dans la table Transactions.
        :param membre_id: ID du membre lié
        :param montant: Montant de la transaction
        :param date: Date de la transaction (format YYYY-MM-DD)
        :param description: Description de la transaction
        :param type_operation: "cotisation", "pret" ou "remboursement"
        :parammois: "en_cours", "annulee" ou "terminee"
        :param pret_id: ID du prêt si type_operation="remboursement", sinon None
        :return: True si succès, False sinon
        """
        try:
            conn = sqlite3.connect('trackfinance.db', timeout=5)
            cursor = conn.cursor()

            cursor.execute(
                '''
                INSERT INTO Transactions(membre_id, pret_id, date, montant, description, type_operation,mois)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (membre_id, pret_id, date, montant, description, type_operation.lower(),mois.lower())
            )
            conn.commit()
            return True

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erreur SQL", f"Erreur d'intégrité : {str(e)}")
            return False
        except sqlite3.OperationalError as e:
            messagebox.showerror("Erreur SQL", f"Erreur opérationnelle : {str(e)}")
            return False
        finally:
            conn.close()


class Prets:
    @staticmethod
    def ajouter_pret(transaction_id, delai, taux_interet, montant_restant):
        """
        Ajoute un prêt dans la table Prets.
        :param transaction_id: ID de la transaction associée (type_operation doit être 'pret')
        :param delai: Durée du prêt en jours/mois (selon ta logique)
        :param taux_interet: Taux d'intérêt en pourcentage (ex: 5.5 pour 5,5 %)
        :param montant_restant: Montant restant dû
        :return: True si succès, False sinon
        """
        try:
            conn = sqlite3.connect('trackfinance.db', timeout=5)
            cursor = conn.cursor()

            # Vérifier que la transaction existe et est bien de type "pret"
            cursor.execute(
                "SELECT type_operation FROM Transactions WHERE id = ? LIMIT 1",
                (transaction_id,)
            )
            transaction = cursor.fetchone()

            if not transaction:
                messagebox.showerror("Erreur", f"La transaction {transaction_id} n'existe pas.")
                return False

            if transaction[0].lower() != "pret":
                messagebox.showerror("Erreur", "La transaction liée n'est pas de type 'pret'.")
                return False

            # Insérer le prêt
            cursor.execute(
                '''
                INSERT INTO Prets(transaction_id, delai, taux_interet, montant_restant)
                VALUES (?, ?, ?, ?)
                ''',
                (transaction_id, delai, taux_interet, montant_restant)
            )
            conn.commit()
            return True

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erreur SQL", f"Erreur d'intégrité : {str(e)}")
            return False
        except sqlite3.OperationalError as e:
            messagebox.showerror("Erreur SQL", f"Erreur opérationnelle : {str(e)}")
            return False
        finally:
            conn.close()
        

def modifier_membre(self):
    # Récupérer l'ID du membre sélectionné
    selected = self.treeview.selection()
    if not selected:
        messagebox.showwarning("Attention", "Veuillez sélectionner un membre à modifier.")
        return

    membre_data = self.treeview.item(selected[0])['values']
    membre_id = membre_data[0]

    # Exemple : ouvrir une fenêtre de saisie avec les valeurs existantes
    update_win = Toplevel(self.root)
    update_win.title("Modifier Membre")
    update_win.geometry("400x400")

    Label(update_win, text="Nom").pack()
    nom_entry = Entry(update_win)
    nom_entry.insert(0, membre_data[1])
    nom_entry.pack()

    Label(update_win, text="Prénom").pack()
    prenom_entry = Entry(update_win)
    prenom_entry.insert(0, membre_data[2])
    prenom_entry.pack()

    Label(update_win, text="Adresse").pack()
    adresse_entry = Entry(update_win)
    adresse_entry.insert(0, membre_data[4])
    adresse_entry.pack()

    Label(update_win, text="Contact").pack()
    contact_entry = Entry(update_win)
    contact_entry.insert(0, membre_data[5])
    contact_entry.pack()

    Label(update_win, text="Mois").pack()
    mois_entry = Entry(update_win)
    mois_entry.insert(0, membre_data[6])
    mois_entry.pack()

    def save_changes():
        try:
            conn = sqlite3.connect("trackfinance.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Membres
                SET name=?, firstname=?, adress=?, contact=?,mois=?
                WHERE id=?
            """, (
                nom_entry.get(),
                prenom_entry.get(),
                adresse_entry.get(),
                contact_entry.get(),
               mois_entry.get(),
                membre_id
            ))
            conn.commit()
            conn.close()

            # Mise à jour du Treeview
            self.treeview.item(selected[0], values=(
                membre_id,
                nom_entry.get(),
                prenom_entry.get(),
                membre_data[3],
                adresse_entry.get(),
                contact_entry.get(),
               mois_entry.get()
            ))

            messagebox.showinfo("Succès", "Membre modifié avec succès ✅")
            update_win.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    Button(update_win, text="Enregistrer", command=save_changes, bg="green", fg="white").pack(pady=20)

def supprimer_membre(self):
    # Récupérer l'ID du membre sélectionné dans le Treeview
    selected = self.treeview.selection()
    if not selected:
        messagebox.showwarning("Attention", "Veuillez sélectionner un membre à supprimer.")
        return

    membre_id = self.treeview.item(selected[0])['values'][0]

    # Confirmation avant suppression
    if not messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer ce membre ?"):
        return

    try:
        conn = sqlite3.connect("trackfinance.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Membres WHERE id=?", (membre_id,))
        conn.commit()
        conn.close()

        # Supprimer la ligne du Treeview
        self.treeview.delete(selected[0])
        messagebox.showinfo("Succès", "Membre supprimé avec succès ✅")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))


