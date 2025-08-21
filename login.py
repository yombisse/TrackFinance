import customtkinter as ctk
import sqlite3
from tkinter import messagebox, END

class Login(ctk.CTkFrame):
    def __init__(self, master, on_success_callback=None):
        super().__init__(master, width=400, height=600, corner_radius=10)
        self.pack_propagate(False)  
        self.place(relx=0.5, rely=0.5, anchor="center")

        self.on_success_callback = on_success_callback
        self.root = master
        self.root.title("Inscription / Connexion")
        ctk.set_appearance_mode("dark")

        # Frame principale pour le contenu des pages
        self.page_frame = ctk.CTkFrame(master=self, width=350, height=450, corner_radius=10)
        self.page_frame.place(relx=0.5, rely=0.55, anchor="center")  # toujours centré

        # Boutons de navigation Login / Signup
        self.login_page_option = ctk.CTkButton(
            master=self, text='Login', font=('Bold', 20), text_color='white',
            width=120, height=40, border_width=2, border_color='white', hover=False,
            command=lambda: self.switch_option('login')
        )
        self.login_page_option.place(relx=0.25, rely=0.1, anchor="center")

        self.signin_page_option = ctk.CTkButton(
            master=self, text='Signup', font=('Bold', 20), text_color='white',
            width=120, height=40, border_width=2, border_color='white', hover=False,
            command=lambda: self.switch_option('signup')
        )
        self.signin_page_option.place(relx=0.75, rely=0.1, anchor="center")

        # On démarre sur la page Signup
        self.switch_option('signup')

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
        heading_lab = ctk.CTkLabel(master=self.page_frame, text='Page de Connexion', font=('bold', 25))
        heading_lab.place(relx=0.5, rely=0.15, anchor="center")

        self.email_entry = ctk.CTkEntry(master=self.page_frame, width=250, height=35, placeholder_text='Email')
        self.email_entry.place(relx=0.5, rely=0.35, anchor="center")

        self.password_entry = ctk.CTkEntry(master=self.page_frame, width=250, height=35,
                                           placeholder_text='Password', show="*")
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")

        login_button = ctk.CTkButton(master=self.page_frame, text='Login', font=('Bold', 20),
                                     text_color='white', width=210, height=40,
                                     border_width=2, border_color='white', hover=False,
                                     command=self.connexion)
        login_button.place(relx=0.5, rely=0.7, anchor="center")

    def signup_page(self):
        heading_lab = ctk.CTkLabel(master=self.page_frame, text="Page d'inscription", font=('bold', 25))
        heading_lab.place(relx=0.5, rely=0.07, anchor="center")

        self.name_entry = ctk.CTkEntry(master=self.page_frame, width=250, height=35, placeholder_text='Nom')
        self.name_entry.place(relx=0.5, rely=0.2, anchor="center")

        self.firstname_entry = ctk.CTkEntry(master=self.page_frame, width=250, height=35, placeholder_text='Prénom')
        self.firstname_entry.place(relx=0.5, rely=0.3, anchor="center")

        self.email_entry = ctk.CTkEntry(master=self.page_frame, width=250, height=35, placeholder_text='Email')
        self.email_entry.place(relx=0.5, rely=0.4, anchor="center")

        self.password_entry = ctk.CTkEntry(master=self.page_frame, width=250, height=35,
                                           placeholder_text='Password', show="*")
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")

        self.password_confirm_entry = ctk.CTkEntry(master=self.page_frame, width=250, height=35,
                                                   placeholder_text='Confirmer Password', show="*")
        self.password_confirm_entry.place(relx=0.5, rely=0.6, anchor="center")

        self.signup_button = ctk.CTkButton(master=self.page_frame, text="S'inscrire", font=('Bold', 20),
                                           text_color='white', fg_color="green", width=210, height=40,
                                           border_width=2, border_color='white', command=self.inscription)
        self.signup_button.place(relx=0.5, rely=0.8, anchor="center")

    def inscription(self):
        name = self.name_entry.get()
        firstname = self.firstname_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
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
            self.email_entry.delete(0, END)
            self.password_entry.delete(0, END)
            self.password_confirm_entry.delete(0, END)
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erreur SQL", f"Cet email existe déjà : {str(e)}")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Erreur SQL", f"Erreur opérationnelle : {str(e)}")
        finally:
            conn.close()

    def connexion(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not (email and password):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        conn = sqlite3.connect('trackfinance.db', timeout=5)
        cursor = conn.cursor()
        cursor.execute('SELECT email, password FROM Users WHERE email=? AND password=?', (email, password))
        user = cursor.fetchone()
        conn.close()

        if not user:
            messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")
        else:
            # Effacer le contenu de la frame (page login)
            # for widget in self.page_frame.winfo_children():
            #     widget.destroy()

            # Label de bienvenue
            ctk.CTkLabel(
                self.page_frame,
                text=f"Bienvenue",
                font=("Bold", 22)
            ).place(relx=0.5, rely=0.8, anchor="center")

            # Progress bar indéterminée (cercle en rotation)
            self.progress = ctk.CTkProgressBar(self.page_frame, width=200)
            self.progress.place(relx=0.5, rely=0.9, anchor="center")
            self.progress.configure(mode="indeterminate")
            self.progress.start()  # pas besoin de paramètre

            # Lancer le dashboard après 2 secondes
            self.after(2000, lambda: self._finish_loading(email))


    def _finish_loading(self, email):
        """Méthode privée : ferme l’animation et ouvre le dashboard"""
        self.progress.stop()
        if self.on_success_callback:
            self.on_success_callback(email)
