from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk, ImageDraw
from datetime import *
import time
import matplotlib.pyplot as plt
import numpy
from App.db import createdb
from App.models import Membre, Transactions,modifier_membre,supprimer_membre
from App.utils import get_dashboard_data
import ttkbootstrap as ttkb
from tkinter import messagebox,filedialog
from ttkbootstrap.constants import *
import sqlite3
from App.models import Prets 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from customtkinter import *
from CTkTable import CTkTable
import customtkinter as ctk
from tkinter import simpledialog
import tkinter as tk
import webbrowser




class TrackFinance:
    def __init__(self, root):
        self.root = root
        self.root.title("TrackFinance")
        self.root.geometry("1366x768")
        set_appearance_mode("dark")  # mode initial
        set_default_color_theme("dark-blue") # thème initial

        self.root.config(bg="#eff5f6")
        self.mainFrame = CTkFrame(master=self.root, bg_color="#eff5f6",width=1366, height=768)
        self.mainFrame.place(x=0, y=0)

        icon = PhotoImage(file=r"C:\Users\HP\Documents\Hori\TrackFinance\icons\logo_icon.png")
        self.root.iconphoto(True, icon)

        # Affiche le Dashboard par défaut
        self.dashboardpage()

        # --- MENU LATERAL ---
        self.FrameMenu = CTkFrame(master=self.root, bg_color="#ffffff", width=250, height=750)
        self.FrameMenu.place(x=0, y=0)

        # Photo de profil
        self.profile_name = Label(self.FrameMenu, text="FANDIE Michel",font=("times new roman",13), bg="#ffffff")
        self.profile_name.place(x=70,y=105)
        image = Image.open(r"C:\Users\HP\Documents\Hori\TrackFinance\icons\profile_icone.png")
        image = image.resize((100, 100))  # redimensionner si besoin
        self.profileImage = ImageTk.PhotoImage(image)

        self.logo = Label(self.FrameMenu, image=self.profileImage)
        self.logo.image = self.profileImage   # garder une référence sinon l’image disparaît
        self.logo.place(x=70, y=0)

        # --- Dashboard (bouton simple) ---

        self.dashboard_selector = Label(self.FrameMenu, text='', bg="#5175da")
        self.dashboard_selector.place(x=65, y=175,width=150, height=2)
        dashboardButton = Button(
            self.FrameMenu, text="🏠 Dashboard", font=("times new roman", 14, "bold"),
            bg="#ffffff", relief="flat",
            command=lambda: self.selector(self.dashboard_selector, self.dashboardpage)
        )
        dashboardButton.place(x=70, y=130)

         # --- Membres (menu déroulant) ---
        self.membres_selector = Label(self.FrameMenu, text='', bg="#5175da")
        self.membres_selector.place(x=65, y=225,width=150, height=2)

        membres_btn = Menubutton(
            self.FrameMenu, text="👥 Membres", bg="#ffffff",
            font=("times new roman", 14, "bold"), relief="flat"
        )
        membres_menu = Menu(membres_btn, tearoff=0)
        membres_menu.add_command(label="➕ Ajouter Membre",font=("times new roman", 12, "bold"), command=lambda: self.selector(self.membres_selector, self.membresform))
        membres_menu.add_command(label="Gestion Membres",font=("times new roman", 12, "bold"), command=lambda:self.selector(self.membres_affichage_selector,self.membres_affichagepage))
        self.membres_affichage_selector = Label(self.FrameMenu, text='', bg="#ffffff")
        self.membres_affichage_selector.place(x=65, y=180, height=45)
        membres_btn["menu"] = membres_menu
        membres_btn.place(x=70, y=180)

        # --- Transactions (menu déroulant) ---
        self.transaction_selector = Label(self.FrameMenu, text='', bg="#5175da")
        self.transaction_selector.place(x=65, y=275,width=150, height=2)

        transaction_btn = Menubutton(
            self.FrameMenu, text="💳 Transactions", bg="#ffffff",
            font=("times new roman", 14, "bold"), relief="flat"
        )
        transaction_menu = Menu(transaction_btn, tearoff=0)
        transaction_menu.add_command(label="➕  Faire une transaction",font=("times new roman", 12, "bold") ,command=lambda: self.selector(self.transaction_selector, self.transactionpage))
        transaction_menu.add_command(label="💳  Mes transactions",font=("times new roman", 12, "bold")  ,command=lambda: self.selector(self.transaction_selector, self.operations_affichagepage))
        transaction_btn["menu"] = transaction_menu
        transaction_btn.place(x=70, y=230)


        # --- Historique (bouton simple) ---
        self.historique_selector = Label(self.FrameMenu, text='', bg="#5175da")
        self.historique_selector.place(x=65, y=175,width=150, height=2)
        HistoriqueButton = Button(
            self.FrameMenu, text="🕒 Historique", font=("times new roman", 14, "bold"),
            bg="#ffffff", relief="flat",
            command=lambda: self.selector(self.historique_selector, self.historiquepage)
        )
        HistoriqueButton.place(x=70, y=280)

        # --- Support (bouton simple) ---

        self.support_selector = Label(self.FrameMenu, text='', bg="#5175da")
        self.support_selector.place(x=65, y=175,width=150, height=2)
        SupportButton = Button(
            self.FrameMenu, text="🏠 Support", font=("times new roman", 14, "bold"),
            bg="#ffffff", relief="flat",
            command=lambda: self.selector(self.support_selector, self.supportpage)
        )
        SupportButton.place(x=70, y=330)

       
    # ///////////// Parametres /////////////
        self.parametre_selector = Label(self.FrameMenu, text='', bg="#5175da")
        self.parametre_selector.place(x=65, y=325,width=150, height=2)
        # button parametre
        parametreButton = Button(
            self.FrameMenu, text="⚙️Paramètres", bg="#ffffff", font=("times new roman", 14, "bold"),
            relief="flat", command=lambda: self.selector(self.parametre_selector, self.parametrepage)
        )
        parametreButton.place(x=70, y=430)
# ///////////// Quitter /////////////
        quitterButton = Button(
            self.FrameMenu, text="❎Quitter", bg="#ffffff", font=("times new roman", 14, "bold"),
            relief="flat", command=quit
        )
        quitterButton.place(x=70, y=480)

         # ///////////// SOLDE /////////////
        self.solde_selector = Label(self.FrameMenu, text='', bg="#5175da")
        self.solde_selector.place(x=65, y=325,width=150, height=2)
        # button solde
        soldeButton = Button(
            self.FrameMenu, text="Solde", bg="#ffffff", font=("times new roman", 14, "bold"),
            relief="flat", command=lambda: self.selector(self.solde_selector, self.soldepage)
        )
        soldeButton.place(x=70, y=380)

        # Sélecteur initial
        self.home_selector()
        # # ///////////// SOLDE /////////////
        # self.solde_selector = Label(self.FrameMenu, text='', bg="#5175da")
        # self.solde_selector.place(x=65, y=325,width=150, height=2)
        # soldeButton = Button(
        #     self.FrameMenu, text="Solde", bg="#ffffff", font=("times new roman", 14, "bold"),
        #     relief="flat", command=lambda: self.selector(self.solde_selector, self.soldepage)
        # )
        # soldeButton.place(x=70, y=480)

    # /////////////// DASHBOARD ///////////////////////////////////
    def dashboardpage(self):
        # cadre(frame) de dashboard
        self.dashboardFrame = CTkFrame(master=self.mainFrame, bg_color="#eff5f6",width=1170, height=750)
        self.dashboardFrame.place(x=250, y=0)

        # Entête
        self.entete = CTkFrame(master=self.dashboardFrame, bg_color="#009df4", width=1170, height=60)
        self.entete.place(x=0, y=0)
        #Nom de l'application
        self.application = Label(
            self.entete, text="📊 TRACKFINANCE", bg="#009df4", font=("times new roman", 16, "bold"),
            bd=0, fg="white", activebackground="#32cf8e"
        )
        self.application.place(x=50, y=15)
        # button deconnexion
        self.deconecte = Button(
            self.entete, text="Deconnecter", bg="#32cf8e", font=("times new roman", 13, "bold"),
            bd=0, fg="white", cursor="hand2", activebackground="#32cf8e"
        )
        self.deconecte.place(x=800, y=15)
 # button notification
        self.notifications = Button(
            self.entete, text="🔔 Notifications", bg="#32cf8e", font=("times new roman", 13, "bold"),
            bd=0, fg="white", cursor="hand2", activebackground="#32cf8e"
        )
        self.notifications.place(x=950, y=15)

        # Label Dashboard
        self.dasboardLabel = Label(
            self.dashboardFrame, text="Bienvenue sur le Tableau de board",
            font=("times new roman", 16, "bold"), bg="#eff5f6"
        )
        self.dasboardLabel.place(x=400, y=70)

   
    # --- Charger les données ---
        data = get_dashboard_data()

        # # # --- Pie Chart : Répartition Cotisations / Prêts / Remboursements ---
        fig = plt.figure(figsize=(5,4.3), dpi=100)
        labels = ["Cotisations", "Prêts", "Remboursements"]
        sizes = [data["total_cotisations"], data["total_prets"], data["total_remboursements"]]
        colors = ["yellowgreen", "gold", "lightcoral"]
        explode = (0.1, 0, 0)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.axis("equal")
        canvabar = FigureCanvasTkAgg(fig, master=self.dashboardFrame)
        canvabar.draw()
        canvabar.get_tk_widget().place(x=300, y=350, anchor=CENTER)
        # --- Bar Chart : Cotisations vs Prêts vs Remboursements vs Bénéfice ---
        figure = plt.figure(figsize=(5,4.3), dpi=100)
        labels = ["Cotisations", "Prêts", "Remboursements", "Bénéfice"]
        values = [data["total_cotisations"], data["total_prets"], data["total_remboursements"], data["benefice"]]
        labelpos = np.arange(len(labels))
        plt.bar(labelpos, values, align="center", alpha=0.8)
        plt.xticks(labelpos, labels, rotation=10, ha="center")
        plt.ylabel("Montants")
        plt.title("Vue d'ensemble des transactions")

        for index, val in enumerate(values):
            plt.text(x=index, y=val+0.5, s=f"{val:.0f}", ha="center")

        canvafig = FigureCanvasTkAgg(figure, master=self.dashboardFrame)
        canvafig.draw()
        canvafig.get_tk_widget().place(x=825, y=350, anchor=CENTER)

        # --- Cartes Résumées ---
        self.diagramme_membreLabel = Label(self.dashboardFrame, text=f"Membres: {data['nb_membres']}", 
                                        fg="white", bg="#f87103", font=("times new roman", 13, "bold"))
        self.diagramme_membreLabel.place(x=100, y=600)

        self.diagramme_pretLabel = Label(self.dashboardFrame, text=f"Prêts: {data['nb_prets']}", 
                                        fg="white", bg="#ecf012", font=("times new roman", 13, "bold"))
        self.diagramme_pretLabel.place(x=350, y=600)

        self.diagramme_ajourLabel = Label(self.dashboardFrame, text=f"Membres à jour: {data['nb_ajour']}", 
                                        fg="white", bg="#088159", font=("times new roman", 13, "bold"))
        self.diagramme_ajourLabel.place(x=600, y=600)

        self.diagramme_beneficeLabel = Label(self.dashboardFrame, text=f"Bénéfice: {data['benefice']}", 
                                            fg="white", bg="#0CA00C", font=("times new roman", 13, "bold"))
        self.diagramme_beneficeLabel.place(x=850, y=600)


    # ---------------- UTILITAIRES ----------------
    def clearselector(self):
        self.dashboard_selector.config(bg="#ffffff")
        self.membres_selector.config(bg="#ffffff")
        self.transaction_selector.config(bg="#ffffff")
        self.solde_selector.config(bg="#ffffff")


    def selector(self, lb, page):
        self.clearselector()
        lb.config(bg="#7aaad1")
        page()

    def home_selector(self):
        self.clearselector()
        self.dashboard_selector.config(bg="#7aaad1")
        

    def set_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.configure(fg_color="grey")

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, END)
                entry.configure(fg_color="white")

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.configure(fg_color="grey")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
       
     

    def statut_value(self, event):
    #      print("Choix du statut :", self.statut_value.get())
        pass

        

        # /////////////// MEMBRES ///////////////////////////////////
    def clear_entries(self):
        self.name_entry.delete(0, END)
        self.firstname_entry.delete(0, END)
        self.date_entry.delete(0, END)
        self.adress_entry.delete(0, END)
        self.contact_entry.delete(0, END)
        self.statut_entry.set("")
        self.set_placeholder(self.date_entry, "YYYY-MM-DD")

    def supprimer_membre(self):
        try:
            # Étape 1 : demander le nom et le prénom
            nom = simpledialog.askstring("Supprimer membre", "Entrez le nom du membre :")
            prenom = simpledialog.askstring("Supprimer membre", "Entrez le prénom du membre :")

            if not nom or not prenom:
                messagebox.showwarning("Attention", "Nom et prénom requis !")
                return

            # Étape 2 : demander le contact
            identifiant = simpledialog.askstring("Supprimer membre", "Entrez le contact du membre :")
            if not identifiant:
                messagebox.showwarning("Attention", "Contact requis !")
                return

            # Requête stricte en ignorant la casse
            conn = sqlite3.connect("trackfinance.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM Membres WHERE name=? COLLATE NOCASE AND firstname=? COLLATE NOCASE AND identifiant=?",
                (nom, prenom, identifiant)
            )
            result = cursor.fetchone()
            conn.close()

            if not result:
                messagebox.showerror("Erreur", "Aucun membre trouvé avec ces informations.")
                return

            membre_id = result[0]

            # Confirmation de suppression
            if not messagebox.askyesno("Confirmer", f"Voulez-vous vraiment supprimer {nom} {prenom} ?"):
                return

            # Suppression
            conn = sqlite3.connect("trackfinance.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Membres WHERE id=?", (membre_id,))
            conn.commit()
            conn.close()

            # Recharger le tableau
            self.filter_members()
            messagebox.showinfo("Succès", f"Membre {nom} {prenom} supprimé ✅")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))




    def modifier_membre(self):
        try:
            # Étape 1 : demander le nom et le prénom
            nom = simpledialog.askstring("Modifier membre", "Entrez le nom du membre :")
            prenom = simpledialog.askstring("Modifier membre", "Entrez le prénom du membre :")

            if not nom or not prenom:
                messagebox.showwarning("Attention", "Nom et prénom requis !")
                return

            # Étape 2 : demander le contact
            identifiant = simpledialog.askstring("Modifier membre", "Entrez l'identifiant(CNIB ou Passeport) du membre :")
            if not identifiant:
                messagebox.showwarning("Attention", "Contact requis !")
                return

            # Requête stricte pour récupérer l'id et les infos
            conn = sqlite3.connect("trackfinance.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id,identifiant,type_identifiant, name, firstname, adress, contact, statut FROM Membres "
                "WHERE name=? COLLATE NOCASE AND firstname=? COLLATE NOCASE AND identifiant=?",
                (nom, prenom, identifiant)
            )
            result = cursor.fetchone()
            conn.close()

            if not result:
                messagebox.showerror("Erreur", "Aucun membre trouvé avec ces informations.")
                return

            membre_id,identifiant,type_identifiant, name, firstname, adress, contact_db, statut = result

            # Fenêtre de modification
            update_win = Toplevel(self.mainFrame)
            update_win.title("Modifier Membre")
            update_win.geometry("400x400")

            CTkLabel(update_win, text="Identifiant", fg_color="#000000",font=("Times New Roman", 14, "bold"), text_color="black").pack()
            identifiant_entry = CTkEntry(update_win)
            identifiant_entry.insert(0, name)
            identifiant_entry.pack()

            type_identifiant_var = ctk.StringVar()
            type_identifiant_entry = ctk.CTkComboBox(
            master=update_win,
            bg_color="#b7d9e9",
            values=["CNIB", "Passeport", "Interne"],
            corner_radius=5,
            width=200,
            variable=type_identifiant_var,
            font=("Times New Roman", 14, "bold"), text_color="black",
            fg_color="#000000"
        )
            type_identifiant_entry.pack()

            CTkLabel(update_win, text="Nom",font=("Times New Roman", 14, "bold"), text_color="black", fg_color="#000000").pack()
            nom_entry = CTkEntry(update_win,corner_radius=5, width=200)
            nom_entry.insert(0, name)
            nom_entry.pack()

            CTkLabel(update_win, text="Prénom",font=("Times New Roman", 14, "bold"), text_color="black", fg_color="#000000").pack()
            prenom_entry = CTkEntry(update_win,corner_radius=5, width=200)
            prenom_entry.insert(0, firstname)
            prenom_entry.pack()

            CTkLabel(update_win, text="Adresse",font=("Times New Roman", 14, "bold"), text_color="black", fg_color="#000000").pack()
            adresse_entry = CTkEntry(update_win,corner_radius=5, width=200)
            adresse_entry.insert(0, adress)
            adresse_entry.pack()

            CTkLabel(update_win, text="Contact",font=("Times New Roman", 14, "bold"), text_color="black", fg_color="#000000").pack()
            contact_entry = CTkEntry(update_win,corner_radius=5, width=200)
            contact_entry.insert(0, contact_db)
            contact_entry.pack()

            statut_var = ctk.StringVar()
            statut_entry = ctk.CTkComboBox(
            master=update_win,
            bg_color="#b7d9e9",
            fg_color="#000000",
            values=["a_jour", "en_retard", "en_pret"],
            corner_radius=5,
            width=200,font=("Times New Roman", 14, "bold"), text_color="black",
            variable=statut_var,
            command=self.statut_value
             )
            statut_entry.pack()
            # Fonction pour enregistrer les modifications
            def save_changes():
                try:
                    conn = sqlite3.connect("trackfinance.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE Membres
                        SET identifiant=?,type_identifiant=?,name=?, firstname=?, adress=?, contact=?, statut=?
                        WHERE id=?
                    """, (
                            identifiant_entry.get().strip(),
                            type_identifiant_var.get().strip(),
                            nom_entry.get().strip(),
                            prenom_entry.get().strip(),
                            adresse_entry.get().strip(),
                            contact_entry.get().strip(),
                            statut_var.get().strip(),

                        membre_id
                    ))
                    conn.commit()
                    conn.close()

                    # Recharger tableau pour voir modifs
                    self.filter_members()
                    messagebox.showinfo("Succès", "Membre modifié avec succès ✅")
                    update_win.destroy()
                except Exception as e:
                    messagebox.showerror("Erreur", str(e))

            Button(update_win, text="Enregistrer", command=save_changes, bg="green", fg="white").pack(pady=20)

        except Exception as e:
            messagebox.showerror("Erreur", str(e))





    def ajouter_membre_interface(self):
        identifiant = self.identifiant_entry.get().strip()
        type_identifiant = self.type_identifiant_var.get().strip()
        name = self.name_entry.get().strip()
        firstname = self.firstname_entry.get().strip()
        date = self.date_entry.get().strip()
        adress = self.adress_entry.get().strip()
        contact = self.contact_entry.get().strip()
        statut = self.statut_var.get().strip()

        if date == "YYYY-MM-DD":
            date = ""

        if not (identifiant and type_identifiant and name and firstname and date and adress and contact and statut):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        Membre.ajouter_membre(identifiant, type_identifiant, name, firstname, date, adress, contact, statut)
        messagebox.showinfo("Succès", f"Membre {name} {firstname} ajouté avec succès.")
        self.clear_entries()


    def membresform(self):
        self.FrameForm = CTkFrame(self.mainFrame, bg_color="#eff5f6", height=750, width=1000)
        self.FrameForm.place(x=250, y=0)
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        CTkLabel(
            master=self.FrameForm, text="Formulaire d'enregistrement d'un membre", text_color="green",
            bg_color="#eff5f6", font=("Times New Roman", 14, "bold")
        ).pack(pady=(20, 30))

        form_frame = CTkFrame(self.FrameForm, bg_color="#cec2e4", corner_radius=5, border_color="blue", border_width=3)
        form_frame.pack(padx=50, pady=50, expand=True)

        def add_row(frame, text, row, entry_widget=None):
            CTkLabel(frame, text=text, font=("Times New Roman", 14, "bold"), text_color="black",
                    bg_color="#cec2e4").grid(row=row, column=0, sticky="w", padx=5, pady=5)
            if entry_widget:
                entry_widget.grid(row=row, column=1, sticky="w", padx=10, pady=5)

        # --- Identifiant unique ---
        self.identifiant_entry = CTkEntry(form_frame, bg_color="#b7d9e9", corner_radius=5, width=200)
        add_row(form_frame, "Identifiant", 0, self.identifiant_entry)

        self.type_identifiant_var = ctk.StringVar()
        self.type_identifiant_entry = ctk.CTkComboBox(
            master=form_frame,
            bg_color="#b7d9e9",
            values=["CNIB", "Passeport", "Interne"],
            corner_radius=5,
            width=200,
            variable=self.type_identifiant_var
        )
        add_row(form_frame, "Type Identifiant", 1, self.type_identifiant_entry)

        self.name_entry = CTkEntry(form_frame, bg_color="#b7d9e9", corner_radius=5, width=200)
        add_row(form_frame, "Nom", 2, self.name_entry)

        self.firstname_entry = CTkEntry(form_frame, bg_color="#b7d9e9", corner_radius=5, width=200)
        add_row(form_frame, "Prénom", 3, self.firstname_entry)

        self.date_entry = CTkEntry(form_frame, bg_color="#b7d9e9", corner_radius=5, width=200)
        add_row(form_frame, "Date d'adhésion", 4, self.date_entry)
        self.set_placeholder(self.date_entry, "YYYY-MM-DD")

        self.adress_entry = CTkEntry(form_frame, bg_color="#b7d9e9", corner_radius=5, width=200)
        add_row(form_frame, "Adresse", 5, self.adress_entry)

        self.contact_entry = CTkEntry(form_frame, bg_color="#b7d9e9", corner_radius=5, width=200)
        add_row(form_frame, "Contact", 6, self.contact_entry)

        self.statut_var = ctk.StringVar()
        self.statut_entry = ctk.CTkComboBox(
            master=form_frame,
            bg_color="#b7d9e9",
            values=["a_jour", "en_retard", "en_pret"],
            corner_radius=5,
            width=200,
            variable=self.statut_var,
            command=self.statut_value
        )
        add_row(form_frame, "Statut", 7, self.statut_entry)

        self.add_button = CTkButton(form_frame, text="Ajouter", bg_color="#064238", corner_radius=10, border_width=2,
                                    command=self.ajouter_membre_interface)
        self.add_button.grid(row=8, column=0, columnspan=2, pady=(20, 5), padx=10, sticky="ew")

    def on_cell_click(self, cell_info):
        # cell_value = valeur de la cellule cliquée
        # tu peux récupérer la ligne ou la colonne si nécessaire
        self.selected_row = cell_info['row']
        print("Cellule cliquée :", cell_info)
        # Par exemple stocker la ligne sélectionnée
        self.selected_row = self.table.get_selected_row()

    def membres_affichagepage(self):
        self.membre_frame = CTkFrame(master=self.mainFrame, bg="#eff5f6", relief="solid")
        self.membre_frame.place(x=250, y=0, width=1100, height=768)

        self.membreLabel = Label(
            self.membre_frame,
            text="LISTE DES MEMBRES",
            font=("Helvetica", 18, "bold"),
            bg="#cce7ff"
        )
        self.membreLabel.place(x=10, y=20)

        # --- Zone recherche ---
        Label(self.membre_frame, text="Recherche Nom+Prénom :", bg="#eff5f6", font=("Arial", 12)).place(x=10, y=60)
        self.search_var = StringVar()
        Entry(self.membre_frame, textvariable=self.search_var, font=("Arial", 12), width=25).place(x=220, y=60)
        Button(self.membre_frame, text="Rechercher", bg="#007acc", fg="white",
            command=self.search_members).place(x=460, y=57)

        # --- Zone filtre ---
        Label(self.membre_frame, text="Filtrer par statut :", bg="#eff5f6", font=("Arial", 12)).place(x=600, y=60)
        self.status_var = StringVar(value="Tous")
        ctk.CTkOptionMenu(self.membre_frame, variable=self.status_var,
                        values=["Tous", "a_jour", "en_pret","en_retard"],
                        command=lambda _: self.filter_members()).place(x=750, y=55)

        self.table_frame = ctk.CTkFrame(self.membre_frame, fg_color="#eff5f6",width=1200, height=450)
        self.table_frame.place(x=10, y=100)


        self.membres_affichage()  # affichage initial

        # --- Boutons ---
        Button(self.membre_frame, text="Supprimer", font=("times new roman", 12, "bold"),
            bg="red", fg="#ffffff", command=self.supprimer_membre).place(x=250, y=600)
        Button(self.membre_frame, text="Modifier", font=("times new roman", 12, "bold"),
            bg="red", fg="#ffffff", command=self.modifier_membre).place(x=400, y=600)
        
    def membres_affichage(self, membres=None):
      #  """Affiche les membres dans CTkTable avec scroll si trop large"""
        if not membres:
            membres = Membre.show_members()  # récup depuis la BD

        # Nettoyer ancien tableau
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        headers = ["ID", "Identifiant", "Type Identifiant", "Nom", "Prénom", "Date d'adhésion", "Adresse", "Contact", "Statut"]
        data = [headers] + [[
            m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8]
        ] for m in membres]

        # ScrollableFrame de CTk
        scroll_frame = CTkScrollableFrame(self.table_frame, width=1000, height=500)  # largeur / hauteur à adapter
        scroll_frame.pack(fill="both", expand=True)

        col_widths = [50, 120, 120, 120, 120, 100, 150, 120, 80]

        self.table = CTkTable(
            scroll_frame,
            row=len(data),
            column=len(headers),
            values=data,
            header_color="#007acc",
            hover_color="#cce7ff",
            command=self.on_cell_click,
            
        )
        self.table.pack(fill="both", expand=True)



    

    def search_members(self):
        """Recherche par nom + prénom"""
        keyword = self.search_var.get().lower()
        all_members = Membre.show_members()
        results = [m for m in all_members if keyword in (m[1] + " " + m[2]).lower()]
        self.membres_affichage(results)


    def filter_members(self):
        """Filtrer par statut"""
        statut = self.status_var.get()
        all_members = Membre.show_members()
        if statut != "Tous":
            results = [m for m in all_members if m[6].lower() == statut.lower()]
        else:
            results = all_members
        self.membres_affichage(results)



    # /////////////// TRANSACTIONS ///////////////////////////////////

    def clear_transaction_entries(self):
        self.membre_var.set("")
        self.montant_entry.delete(0, END)
        self.date_trans_entry.delete(0, END)
        self.description_entry.delete(0, END)
        self.type_var.set("")
        self.mois_var.set("")
        
        # Champs spécifiques prêt
        self.delai_entry.delete(0, END)
        self.taux_entry.delete(0, END)
        self.montant_restant_entry.delete(0, END)
    
    # Champ spécifique remboursement
        self.pret_var.set("")

    def transactionpage(self):
        self.FrameForm = CTkFrame(master=self.mainFrame, bg_color="#eff5f6", width=1170, height=750)
        self.FrameForm.place(x=250, y=0)

        Label(self.FrameForm, text="Formulaire d'ajout de transaction",
            font=("Helvetica", 24), bg="#eff5f6", fg="white", relief="groove").pack(pady=(20, 30))

        form_frame = CTkFrame(master=self.FrameForm, bg_colr="#b7bdbd", bd=2, relief="solid")
        form_frame.pack(padx=20, pady=20, expand=True)

        # ---------- StringVars ----------
        self.type_var = StringVar(master=self.root)
        self.membre_var = StringVar(master=self.root)
        self.mois_var = StringVar(master=self.root)
        self.pret_var = StringVar(master=self.root)

        # ---------- Widgets ----------
        def add_row(frame, text, row, widget=None):
            Label(frame, text=text, font=("Times New Roman", 14, "bold"),
                bg="#b7bdbd").grid(row=row, column=0, sticky="w", padx=10, pady=5)
            if widget:
                widget.grid(row=row, column=1, sticky="w", padx=10, pady=5)

        # Type d'opération
        self.type_entry = CTkComboBox(master=form_frame, variable=self.type_var,bg_color="#b7bdbd",
                                    values=["cotisation", "pret", "remboursement"],command=self.toggle_fields)
        
        add_row(form_frame, "Type d'opération", 4, self.type_entry)

        # Membre
        membres_list = [m[0] for m in Membre.get_all_names()]
        self.membre_entry = CTkComboBox(
            master=form_frame,bg_color="#b7bdbd",values=membres_list,variable=self.membre_var,command=self.statut_value
            
        )
        
        add_row(form_frame, "Nom du Membre", 0, self.membre_entry)

        # Montant
        self.montant_entry = Entry(form_frame)
        add_row(form_frame, "Montant", 1, self.montant_entry)

        # Date
        self.date_trans_entry = Entry(form_frame)
        add_row(form_frame, "Date (YYYY-MM-DD)", 2, self.date_trans_entry)

        # Description
        self.description_entry = Entry(form_frame)
        add_row(form_frame, "Description", 3, self.description_entry)

        # Statut
        self.mois_entry = CTkComboBox(master=form_frame, variable=self.mois_var,
                                        values=["Janvier", "Fevrier", "Mars","Avril", "Mai", "Juin","Juillet", "Aout", "Septembre","Octobre", "Novembre", "Decembre"])
        add_row(form_frame, "mois", 5, self.mois_entry)

        # Champs prêt
        self.frame_pret = CTkFrame(master=form_frame, bg_color="#b7bdbd")
        Label(self.frame_pret, text="Délai", bg="#b7bdbd",font=("Times New Roman", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.delai_entry = Entry(self.frame_pret)
        self.delai_entry.grid(row=0, column=1)
        Label(self.frame_pret, text="Taux d'intérêt (%)", bg="#b7bdbd",font=("Times New Roman", 12, "bold")).grid(row=1, column=0, padx=5, pady=5)
        self.taux_entry = Entry(self.frame_pret)
        self.taux_entry.grid(row=1, column=1)
        Label(self.frame_pret, text="Montant restant", bg="#b7bdbd",font=("Times New Roman", 12, "bold")).grid(row=2, column=0, padx=5, pady=5)
        self.montant_restant_entry = Entry(self.frame_pret)
        self.montant_restant_entry.grid(row=2, column=1)

        # Champs remboursement
        self.frame_remboursement = CTkFrame(master=form_frame, bg="#b7bdbd")
        Label(self.frame_remboursement, text="Sélectionner le prêt", bg="#b7bdbd",font=("Times New Roman", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)

        # Récupérer les prêts depuis la DB
        conn = sqlite3.connect('trackfinance.db')
        cursor = conn.cursor()
        cursor.execute("SELECT transaction_id FROM Prets")  # ID de la transaction prêt
        prets_list = [str(p[0]) for p in cursor.fetchall()]
        conn.close()

        self.pret_entry = CTkComboBox(master=self.frame_remboursement, variable=self.pret_var, values=prets_list)
        self.pret_entry.grid(row=0, column=1)
        self.pret_var.trace("w", self.remplir_champs_remboursement)

        # Bouton Ajouter
        Button(form_frame, text="Ajouter", bg="green", fg="white",
            command=self.ajouter_transaction_interface).grid(row=10, column=0, columnspan=2, pady=20, sticky="ew")

    def toggle_fields(self, event):
        type_op = self.type_var.get()

        # Cacher tous les frames spécifiques
        self.frame_pret.grid_forget()
        self.frame_remboursement.grid_forget()

        # Afficher le frame correspondant
        if type_op == "pret":
            self.frame_pret.grid(row=6, column=0, columnspan=2, pady=10)
        elif type_op == "remboursement":
            self.frame_remboursement.grid(row=6, column=0, columnspan=2, pady=10)


    # ---------- Fonction pour récupérer le nom d'un membre à partir de son ID ----------
    def get_membre_name(self, membre_id):
        conn = sqlite3.connect("trackfinance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Membres WHERE id=?", (membre_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        return ""

    # ---------- Fonction de remplissage dynamique ----------
    def remplir_champs_remboursement(self, *args):
        pret_id = self.pret_var.get().strip()
        if not pret_id:
            return

        conn = sqlite3.connect("trackfinance.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.membre_id, t.montant, t.date, t.description, p.taux_interet
            FROM Transactions t
            JOIN Prets p ON t.id = p.transaction_id
            WHERE t.id = ?
        """, (pret_id,))
        pret = cursor.fetchone()
        conn.close()

        if pret:
            membre_id_pret, montant_pret, date_pret, description_pret, taux_interet = pret
            montant_total = round(montant_pret * (1 + taux_interet / 100), 2)

            # Remplissage automatique des champs
            self.membre_var.set(self.get_membre_name(membre_id_pret))
            self.montant_entry.delete(0, END)
            self.montant_entry.insert(0, str(montant_total))
            self.date_trans_entry.delete(0, END)
            self.date_trans_entry.insert(0, date_pret)
            self.description_entry.delete(0, END)
            self.description_entry.insert(0, description_pret)

    # ---------- Fonction d'ajout de transaction ----------
    def ajouter_transaction_interface(self):
        membre_nom = self.membre_var.get().strip()
        montant = self.montant_entry.get().strip()
        date = self.date_trans_entry.get().strip()
        description = self.description_entry.get().strip()
        type_operation = self.type_var.get().strip()
        mois = self.mois_var.get().strip()

        if not (membre_nom and date and type_operation and mois):
            messagebox.showerror("Erreur", "Tous les champs obligatoires doivent être remplis.")
            return

        conn = sqlite3.connect("trackfinance.db")
        cursor = conn.cursor()

        # Récupérer ID membre
        cursor.execute("SELECT id FROM Membres WHERE name=? LIMIT 1", (membre_nom,))
        result = cursor.fetchone()
        if result is None:
            messagebox.showerror("Erreur", f"Membre '{membre_nom}' introuvable.")
            return
        membre_id = result[0]

        pret_id = None

        # ------ Cas spécifiques ------
        if type_operation == "pret":
            delai = self.delai_entry.get().strip()
            taux = self.taux_entry.get().strip()
            montant_restant = self.montant_restant_entry.get().strip()

            if not (montant and delai and taux and montant_restant):
                messagebox.showerror("Erreur", "Tous les champs de prêt doivent être remplis.")
                return
 
            cursor.execute("SELECT SUM(montant) FROM Transactions WHERE membre_id=? AND type_operation='cotisation'", (membre_id,))
            total_cotisations = cursor.fetchone()[0] or 0

            if float(montant) > total_cotisations:
                messagebox.showerror("Erreur", f" Désolé, nous ne pouvons pas vous accorder ce pret pour le moment.Le prêt demandé ({montant}) dépasse vos cotisations totales ({total_cotisations}).")
                return

            cursor.execute("""
                INSERT INTO Transactions (membre_id, montant, date, description, type_operation, mois)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (membre_id, montant, date, description, type_operation, mois))
            pret_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO Prets (transaction_id, delai, taux_interet, montant_restant)
                VALUES (?, ?, ?, ?)
            """, (pret_id, delai, taux, montant_restant))

        elif type_operation == "remboursement":
            pret_id = self.pret_var.get().strip()
            if not pret_id:
                messagebox.showerror("Erreur", "Veuillez sélectionner le prêt à rembourser.")
                return

            # Les champs ont déjà été remplis dynamiquement
            montant = self.montant_entry.get().strip()
            description = self.description_entry.get().strip()
            date = self.date_trans_entry.get().strip()

            cursor.execute("""
                INSERT INTO Transactions (membre_id, pret_id, montant, date, description, type_operation, mois)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (membre_id, pret_id, montant, date, description, type_operation, mois))

        else:  # Cotisation
            if not montant:
                messagebox.showerror("Erreur", "Le montant doit être renseigné.")
                return
            cursor.execute("""
                INSERT INTO Transactions (membre_id, montant, date, description, type_operation, mois)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (membre_id, montant, date, description, type_operation, mois))

        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", f"{type_operation.capitalize()} ajouté avec succès ✅")
        self.clear_transaction_entries()



    
    def operations_affichagepage(self):
        self.operation_frame = CTkFrame(self.mainFrame, fg_color="#b7bdbd", corner_radius=10, width=1100, height=768)
        self.operation_frame.place(x=250, y=0)
        

        CTkLabel(
            self.operation_frame,
            text="LISTE DES OPÉRATIONS",
            font=("Helvetica", 18, "bold"),
            text_color="black"
        ).place(x=10, y=20)

        # Zone recherche + filtre
        CTkLabel(self.operation_frame, text="Rechercher :", font=("Helvetica", 12)).place(x=130, y=70)
        self.search_entry = CTkEntry(self.operation_frame, placeholder_text="Nom du membre")
        self.search_entry.place(x=120, y=70)
        CTkButton(self.operation_frame, text="Rechercer", command=self.filter_operations).place(x=200, y=70)


        CTkLabel(self.operation_frame, text="Filtrer par type :", font=("Helvetica", 12)).place(x=400, y=70)
        self.type_var = StringVar(master=self.root)
        self.filter_var = StringVar(value="Tous")
        self.filter_combo = CTkComboBox(
            self.operation_frame,
            values=["Tous", "Prêt", "Cotisation", "Remboursement"],
            variable=self.filter_var
        )
        self.filter_combo.place(x=480, y=70 )

        CTkButton(self.operation_frame, text="Appliquer", command=self.filter_operations).place(x=700, y=70)

        # Boutons actions
        CTkButton(self.operation_frame, text="Supprimer", fg_color="red", command=self.supprimer_operation).place(x=500, y=500)
        CTkButton(self.operation_frame, text="Modifier", fg_color="orange", command=self.modifier_operation).place(x=700, y=500)

        # Cadre pour la table
        self.table_frame = CTkFrame(self.operation_frame,width=1000)
        self.table_frame.place(x=10, y=120)

        self.operations_affichage()  # affichage initial


    def operations_affichage(self):
        # Charger toutes les opérations
        
        conn = sqlite3.connect("trackfinance.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, m.name || ' ' || m.firstname, t.type_operation, t.montant, t.date, t.description, t.mois, t.pret_id
            FROM Transactions t
            JOIN Membres m ON t.membre_id = m.id
            ORDER BY t.date DESC
        """)
        transactions = cursor.fetchall()
        conn.close()

        # Colonnes
        headers = ["ID", "Membre", "Type", "Montant", "Date", "Description", "Mois", "Prêt ID"]

        # Nettoyer ancien tableau
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Création du tableau
        self.table = CTkTable(
            master=self.table_frame,
            row=len(transactions)+1,
            column=len(headers),
            values=[headers] + list(transactions),
            header_color="#007acc",
            hover_color="#cce7ff",
            corner_radius=10
        )
        self.table.pack(expand=True)


    def filter_operations(self):
        search_term = self.search_entry.get().lower()
        filter_type = self.filter_var.get()

        conn = sqlite3.connect("trackfinance.db")
        cursor = conn.cursor()

        query = """
            SELECT t.id, m.name || ' ' || m.firstname, t.type_operation, t.montant, t.date, t.description, t.mois, t.pret_id
            FROM Transactions t
            JOIN Membres m ON t.membre_id = m.id
            WHERE (m.name LIKE ? OR m.firstname LIKE ?)
        """
        params = (f"%{search_term}%", f"%{search_term}%")

        if filter_type != "Tous":
            query += " AND t.type_operation=?"
            params += (filter_type,)

        query += " ORDER BY t.date DESC"

        cursor.execute(query, params)
        transactions = cursor.fetchall()
        conn.close()

        headers = ["ID", "Membre", "Type", "Montant", "Date", "Description", "Mois", "Prêt ID"]

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.table = CTkTable(
            master=self.table_frame,
            row=len(transactions)+1,
            column=len(headers),
            values=[headers] + list(transactions),
            header_color="#007acc",
            hover_color="#cce7ff",
            corner_radius=10
        )
        self.table.pack(expand=True, fill="both")



    def choisir_membre(self):
        # Nom et prénom (ignorant la casse)
        nom = simpledialog.askstring("Membre", "Entrez le nom du membre :")
        if not nom:
            return None
        prenom = simpledialog.askstring("Membre", "Entrez le prénom du membre :")
        if not prenom:
            return None

        # Identifiant (sensible à la casse)
        identifiant = simpledialog.askstring("Membre", "Entrez l'identifiant du membre :")
        if not identifiant:
            return None

        # Rechercher le membre
        conn = sqlite3.connect("trackfinance.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM Membres 
            WHERE LOWER(name)=? AND LOWER(firstname)=? AND identifiant=?
        """, (nom.lower(), prenom.lower(), identifiant))
        result = cursor.fetchone()
        conn.close()

        if not result:
            messagebox.showerror("Erreur", "Membre introuvable avec ces informations.")
            return None

        return result[0]  # id du membre

    def get_operations_du_membre(self, membre_id):
        conn = sqlite3.connect("trackfinance.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, type_operation, montant, description, mois 
            FROM Transactions WHERE membre_id=?
        """, (membre_id,))
        ops = cursor.fetchall()
        conn.close()
        return ops

    def supprimer_operation(self):
        membre_id = self.choisir_membre()
        if not membre_id:
            return

        ops = self.get_operations_du_membre(membre_id)
        if not ops:
            messagebox.showinfo("Info", "Ce membre n'a aucune opération.")
            return

        # Menu déroulant pour choisir l'opération
        op_dict = {f"{op[1]} - {op[2]} ({op[3]}) [{op[4]}]": op[0] for op in ops}
        choix_var = StringVar(value=list(op_dict.keys())[0])

        choix_win = CTkToplevel(self.mainFrame)
        choix_win.title("Choisir opération")
        choix_win.geometry("400x200")
        CTkLabel(choix_win, text="Sélectionnez l'opération :").pack(pady=10)
        CTkOptionMenu(choix_win, variable=choix_var, values=list(op_dict.keys())).pack(pady=10)

        def valider():
            op_id = op_dict[choix_var.get()]
            if not messagebox.askyesno("Confirmer", "Voulez-vous vraiment supprimer cette opération ?"):
                return
            conn = sqlite3.connect("trackfinance.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Transactions WHERE id=?", (op_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Opération supprimée ✅")
            self.filter_operations()
            choix_win.destroy()

        CTkButton(choix_win, text="Supprimer", fg_color="red", command=valider).pack(pady=20)

    def modifier_operation(self):
        membre_id = self.choisir_membre()
        if not membre_id:
            return

        ops = self.get_operations_du_membre(membre_id)
        if not ops:
            messagebox.showinfo("Info", "Ce membre n'a aucune opération.")
            return

        # Menu déroulant pour choisir l'opération
        op_dict = {f"{op[1]} - {op[2]} ({op[3]}) [{op[4]}]": op for op in ops}
        choix_var = StringVar(value=list(op_dict.keys())[0])

        choix_win = CTkToplevel(self.mainFrame)
        choix_win.title("Choisir opération")
        choix_win.geometry("400x200")
        CTkLabel(choix_win, text="Sélectionnez l'opération :").pack(pady=10)
        CTkOptionMenu(choix_win, variable=choix_var, values=list(op_dict.keys())).pack(pady=10)

        def modifier():
            op_data = op_dict[choix_var.get()]
            op_id = op_data[0]
            type_op = op_data[1]

            update_win = CTkToplevel(self.mainFrame)
            update_win.title("Modifier Opération")
            update_win.geometry("400x500")

            # --- Type (non modifiable) ---
            CTkLabel(update_win, text="Type").pack(pady=5)
            type_label = CTkLabel(update_win, text=type_op)
            type_label.pack()

            # --- Montant ---
            CTkLabel(update_win, text="Montant").pack(pady=5)
            montant_entry = CTkEntry(update_win)
            montant_entry.insert(0, op_data[2])
            montant_entry.pack()

            # --- Description ---
            CTkLabel(update_win, text="Description").pack(pady=5)
            desc_entry = CTkEntry(update_win)
            desc_entry.insert(0, op_data[3])
            desc_entry.pack()

            # --- Mois ---
            CTkLabel(update_win, text="Mois").pack(pady=5)
            mois_entry = CTkEntry(update_win)
            mois_entry.insert(0, op_data[4])
            mois_entry.pack()

            def save_changes():
                montant = float(montant_entry.get())

                # --- Vérification si c'est un prêt ---
                if type_op == "pret":
                    conn = sqlite3.connect("trackfinance.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT SUM(montant) FROM Transactions WHERE membre_id=? AND type_operation='cotisation'", (membre_id,))
                    total_cotisations = cursor.fetchone()[0] or 0
                    conn.close()

                    if montant > total_cotisations:
                        messagebox.showerror(
                            "Erreur",
                            f"Le montant du prêt ({montant}) dépasse vos cotisations totales ({total_cotisations})."
                        )
                        return

                # --- Mise à jour ---
                conn = sqlite3.connect("trackfinance.db")
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Transactions
                    SET montant=?, description=?, mois=?
                    WHERE id=?
                """, (
                    montant,
                    desc_entry.get(),
                    mois_entry.get(),
                    op_id
                ))
                conn.commit()
                conn.close()

                self.filter_operations()
                messagebox.showinfo("Succès", "Opération modifiée ✅")
                update_win.destroy()
                choix_win.destroy()

            CTkButton(update_win, text="Enregistrer", fg_color="green", command=save_changes).pack(pady=20)

        CTkButton(choix_win, text="Modifier", fg_color="blue", command=modifier).pack(pady=20)



# /////////////// Historique ///////////////////////////////////

    def historiquepage(self):
        # Création du frame
        self.historiqueFrame = CTkFrame(self.mainFrame, width=1170, height=750)
        self.historiqueFrame.place(x=250, y=0)

        CTkLabel(self.historiqueFrame, text="Historique complet",
                font=("times new roman", 16, "bold")).place(x=480, y=20)

        # Nettoyer ancien tableau si présent
        for widget in self.mainFrame.winfo_children():
            if isinstance(widget, CTkTable):
                widget.destroy()

        conn = sqlite3.connect("trackfinance.db")
        cursor = conn.cursor()

        # Récupérer transactions financières
        cursor.execute("""
            SELECT id, 'Transaction' as type, type_operation as action, montant, description, date
            FROM Transactions
        """)
        transactions = cursor.fetchall()

        # Récupérer actions sur les membres
        cursor.execute("""
            SELECT id, 'Membre' as type, action, NULL as montant, description, date
            FROM HistoriqueMembre
        """)
        membres_ops = cursor.fetchall()

        # Combiner et trier par date
        historique = sorted(transactions + membres_ops, key=lambda x: x[5])

        conn.close()

        # Préparer données pour CTkTable
        headers = ["ID", "Catégorie", "Action", "Montant", "Description", "Date"]
        data = [headers] + [list(row) for row in historique]

        self.historiqueTable = CTkTable(
            self.historiqueFrame,
            row=len(data),
            column=len(headers),
            values=data,
            header_color="#007acc",
            hover_color="#cce7ff"
        )
        self.historiqueTable.pack(fill="both", expand=True)



# /////////////// SUPPORT ///////////////////////////////////

    


    def supportpage(self):
        # Frame de support
        self.supportFrame = CTkFrame(self.mainFrame, width=1170, height=750)
        self.supportFrame.place(x=250, y=0)

        # Titre
        CTkLabel(self.supportFrame, text="Support et contacts",
                font=("times new roman", 16, "bold")).place(x=500, y=50)

        # Boutons réseaux / email
        def open_facebook():
            webbrowser.open("https://www.facebook.com/tonprofil")

        def open_linkedin():
            webbrowser.open("https://www.linkedin.com/in/tonprofil")

        def open_gmail():
            webbrowser.open("mailto:tonemail@gmail.com")

        CTkButton(self.supportFrame, text="Facebook", width=200, command=open_facebook).place(x=500, y=150)
        CTkButton(self.supportFrame, text="LinkedIn", width=200, command=open_linkedin).place(x=500, y=220)
        CTkButton(self.supportFrame, text="Gmail", width=200, command=open_gmail).place(x=500, y=290)

        # /////////////// SOLDE ///////////////////////////////////


    def soldepage(self):
        # Créer le frame pour la page Solde
        self.soldeFrame = CTkFrame(self.mainFrame, width=1170, height=750, bg_color="#eff5f6")
        self.soldeFrame.place(x=250, y=0)

        # Récupérer les données financières
        finances = self.calcul_finances()

        # Titre
        CTkLabel(self.soldeFrame, text="Solde et finances", font=("times new roman", 16, "bold")).place(x=500, y=50)
        data = get_dashboard_data()
        # Affichage des informations
        CTkLabel(self.soldeFrame, text=f"Somme disponible (cotisations) : {finances['somme_disponible']}").place(x=400, y=150)
        CTkLabel(self.soldeFrame, text=f"Somme en prêt non remboursée : {finances['pret_non_remboursse']}").place(x=400, y=200)
        CTkLabel(self.soldeFrame, text=f"Total finances : {finances['total_finances']}").place(x=400, y=250)
        CTkLabel(self.soldeFrame, text=f"Nombre de membres : {finances['nb_membres']}").place(x=400, y=300)
        CTkLabel(self.soldeFrame, text=f"Prêts en cours : {finances['nb_prets_en_cours']}").place(x=400, y=350)
        CTkLabel(self.soldeFrame, text=f"Prêts rembourses : {finances['somme_rembourssement']}").place(x=400, y=400)
        CTkLabel(self.soldeFrame, text=f"Bénéfice : {data["benefice"]}").place(x=400, y=450)


    def calcul_finances(self):
        data = get_dashboard_data()
        self.benefice=data["benefice"]
        conn = sqlite3.connect("trackfinance.db")
        cursor = conn.cursor()

        # Somme de toutes les cotisations
        cursor.execute("""
            SELECT IFNULL(SUM(montant),0) 
            FROM Transactions 
            WHERE type_operation='cotisation'
        """)
        somme_disponible = cursor.fetchone()[0]

        # Somme des prêts non remboursés
        cursor.execute("""
            SELECT IFNULL(SUM(montant),0) 
            FROM Transactions 
            WHERE type_operation='pret'
        """)
        somme_en_pret = cursor.fetchone()[0]

        # Somme des prêts  remboursés
        cursor.execute("""
            SELECT IFNULL(SUM(montant),0) 
            FROM Transactions 
            WHERE type_operation='remboursement'
        """)
        somme_remboursement = cursor.fetchone()[0]

        pret_non_remboursse=somme_en_pret-somme_remboursement
        
        # Total disponible pour l'application
        total_finances = somme_disponible + somme_en_pret

        # Nombre de membres
        cursor.execute("SELECT COUNT(*) FROM Membres")
        nb_membres = cursor.fetchone()[0]

        # Nombre de prêts en cours
        cursor.execute("SELECT COUNT(*) FROM Prets WHERE montant_restant > 0")
        nb_prets_en_cours = cursor.fetchone()[0]
        
        conn.close()

        return {
            "somme_disponible": somme_disponible,
            "somme_en_pret": somme_en_pret,
            "total_finances": total_finances,
            "nb_membres": nb_membres,
            "nb_prets_en_cours": nb_prets_en_cours,
            "pret_non_remboursse":pret_non_remboursse,
            "somme_rembourssement":somme_remboursement
           
        }

        # /////////////// PARAMETRES ///////////////////////////////////

    def parametrepage(self):
        
        # Supprimer les anciens widgets de mainFrame
        for widget in self.mainFrame.winfo_children():
            if isinstance(widget, ctk.CTkFrame) or (isinstance(widget, tk.Frame) and widget != self.FrameMenu):
                widget.destroy()

        # Frame Paramètres
        self.parametreFrame = ctk.CTkFrame(self.mainFrame, width=1170, height=750)
        self.parametreFrame.place(x=250, y=0)

        # Label
        ctk.CTkLabel(self.parametreFrame, text="Personnaliser votre application",
                    font=("times new roman", 14, "bold")).place(x=450, y=50)

        # Bouton toggle thème
        self.theme_toggle = ctk.CTkButton(self.parametreFrame, text="Changer de thème 🌞/🌙",
                                        command=self.toggle_theme)
        self.theme_toggle.place(x=500, y=150)

        # Slider luminosité
        ctk.CTkLabel(self.parametreFrame, text="Luminosité").place(x=60, y=60)
        self.slider = ctk.CTkSlider(self.parametreFrame, from_=0.3, to=1.0,
                                    command=self.brightness, width=200)
        self.slider.set(1.0)
        self.slider.place(x=150, y=60)
        self.mode="dark"
    def toggle_theme(self):
        self.mode
        
        if self.mode == "dark":
            set_appearance_mode("light")
            self.mode="light"
        else:
            set_appearance_mode("dark")
            self.mode="dark"
        

    def brightness(self, value):
        brightness = int(255 * value)
        color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"

        for frame in self.mainFrame.winfo_children():
            if isinstance(frame, ctk.CTkFrame):
                frame.configure(fg_color=color)
                self.apply_brightness_recursive(frame, color)

    def apply_brightness_recursive(self, parent, color):
        for widget in parent.winfo_children():
            try:
                widget.configure(fg_color=color)
            except:
                pass
            if isinstance(widget, ctk.CTkFrame):
                self.apply_brightness_recursive(widget, color)



if __name__ == "__main__":
    createdb()
  
   
    root = CTk()
    TrackFinance(root)
    root.mainloop()


import customtkinter as ctk
import sqlite3
from tkinter import messagebox, END


# ============================
# Fenêtre principale TrackFinance
# ============================
class TrackFinanceApp:
    def __init__(self, root, user_email):
        self.root = root
        self.root.title("TrackFinance - Tableau de bord")
        self.root.geometry("900x600")
        self.root.configure(bg="black")
        ctk.set_appearance_mode("dark")

        # Exemple tableau de bord
        label = ctk.CTkLabel(self.root, text=f"Bienvenue dans TrackFinance, {user_email} !",
                             font=("Arial", 20), text_color="white")
        label.pack(pady=40)

        # Ici tu pourras ajouter tes pages : Membres, Transactions, Prêts, etc.


# ============================
# Fenêtre de login/signup
# ============================
class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Inscription / Connexion")
        self.root.geometry("400x600")
        self.root.resizable(width=False, height=True)
        self.root.configure(bg='black')
        ctk.set_appearance_mode('dark')

        # Démarrer sur signup
        self.signup_page()

        # Boutons de navigation
        self.login_page_option = ctk.CTkButton(
            master=self.root, text='Login', font=('Bold', 20), text_color='white',
            width=120, height=40, border_width=2, border_color='white', hover=False,
            command=lambda: self.switch_option('login')
        )
        self.login_page_option.place(x=75, y=90)

        self.signin_page_option = ctk.CTkButton(
            master=self.root, text='Signup', font=('Bold', 20), text_color='white',
            width=120, height=40, border_width=2, border_color='white', hover=False,
            command=lambda: self.switch_option('signup')
        )
        self.signin_page_option.place(x=205, y=90)

    def switch_option(self, switch_to):
        for widget in self.page_frame.winfo_children():
            widget.destroy()

        if switch_to == 'login':
            self.signin_page_option.configure(fg_color='white', text_color='black')
            self.login_page_option.configure(fg_color='#1F6AA5', text_color='black')
            self.login_page()
        else:
            self.login_page_option.configure(fg_color='white', text_color='black')
            self.signin_page_option.configure(fg_color='#1F6AA5', text_color='black')
            self.signup_page()

    def login_page(self):
        self.page_frame = ctk.CTkFrame(master=self.root, width=250, height=400, corner_radius=10)
        self.page_frame.place(x=75, y=160)

        heading_lab = ctk.CTkLabel(master=self.page_frame, text='Page de Connexion', font=('bold', 25))
        heading_lab.place(x=10, y=50)

        self.login_email_entry = ctk.CTkEntry(master=self.page_frame, width=230, height=35,
                                              placeholder_text='Email')
        self.login_email_entry.place(x=10, y=100)

        self.login_password_entry = ctk.CTkEntry(master=self.page_frame, width=230, height=35,
                                                 placeholder_text='Password', show="*")
        self.login_password_entry.place(x=10, y=150)

        login_button = ctk.CTkButton(master=self.page_frame, text='Login', font=('Bold', 20),
                                     text_color='white', width=210, height=40,
                                     border_width=2, border_color='white', hover=False,
                                     command=self.connexion)
        login_button.place(x=20, y=210)

    def signup_page(self):
        self.page_frame = ctk.CTkFrame(master=self.root, width=250, height=400, corner_radius=10)
        self.page_frame.place(x=75, y=160)

        heading_lab = ctk.CTkLabel(master=self.page_frame, text="Page d'inscription", font=('bold', 25))
        heading_lab.place(x=10, y=20)

        self.name_entry = ctk.CTkEntry(master=self.page_frame, width=230, height=35, placeholder_text='Nom')
        self.name_entry.place(x=10, y=100)

        self.firstname_entry = ctk.CTkEntry(master=self.page_frame, width=230, height=35, placeholder_text='Prénom')
        self.firstname_entry.place(x=10, y=150)

        self.signup_email_entry = ctk.CTkEntry(master=self.page_frame, width=230, height=35, placeholder_text='Email')
        self.signup_email_entry.place(x=10, y=200)

        self.signup_password_entry = ctk.CTkEntry(master=self.page_frame, width=230, height=35,
                                                  placeholder_text='Password', show="*")
        self.signup_password_entry.place(x=10, y=250)

        self.password_confirm_entry = ctk.CTkEntry(master=self.page_frame, width=230, height=35,
                                                   placeholder_text='Confirmer Password', show="*")
        self.password_confirm_entry.place(x=10, y=300)

        self.signup_button = ctk.CTkButton(master=self.page_frame, text="S'inscrire", font=('Bold', 20),
                                           text_color='white', fg_color="green", width=210, height=40,
                                           border_width=2, border_color='white', command=self.inscription)
        self.signup_button.place(x=20, y=350)

    def inscription(self):
        name = self.name_entry.get()
        firstname = self.firstname_entry.get()
        email = self.signup_email_entry.get()
        password = self.signup_password_entry.get()
        password_confirm = self.password_confirm_entry.get()

        if not (name and firstname and email and password and password_confirm):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        if password != password_confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        try:
            conn = sqlite3.connect('trackfinance.db', timeout=5)
            cursor = conn.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                firstname TEXT,
                                email TEXT UNIQUE,
                                password TEXT)''')

            cursor.execute('INSERT INTO Users(name, firstname, email, password) VALUES (?, ?, ?, ?)',
                           (name, firstname, email, password))
            conn.commit()
            messagebox.showinfo("Succès", f"Utilisateur {name} {firstname} ajouté avec succès.")

            self.name_entry.delete(0, END)
            self.firstname_entry.delete(0, END)
            self.signup_email_entry.delete(0, END)
            self.signup_password_entry.delete(0, END)
            self.password_confirm_entry.delete(0, END)

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erreur SQL", f"Cet email existe déjà : {str(e)}")
        finally:
            conn.close()

    def connexion(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        if not (email and password):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        conn = sqlite3.connect('trackfinance.db', timeout=5)
        cursor = conn.cursor()

        cursor.execute('SELECT email FROM Users WHERE email=? AND password=?', (email, password))
        user = cursor.fetchone()
        conn.close()

        if not user:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")
        else:
            messagebox.showinfo("Succès", f"Bienvenue {email} !")
            self.root.destroy()  # fermer la fenêtre login

            # Ouvrir le dashboard principal
            app_root = ctk.CTk()
            TrackFinanceApp(app_root, email)
            app_root.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    Login(root)
    root.mainloop()
