import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import hashlib
import subprocess
from datetime import datetime
from fpdf import FPDF



path = "games"

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.title("App de Connexion")
        self.geometry("1280x720")

        # Capture de l'événement de fermeture de la fenêtre principale
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialiser la session utilisateur
        self.current_user = None
        self.session_start_time = None
        self.scores_data = {
            "color_game": 0,
            "calculation_game": 0,
            "path_game": 0
        }

        # Créer le frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Créer un système d'onglets
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        # Ajouter des onglets
        self.tabview.add("Accueil")
        self.tabview.add("Inscription")
        self.tabview.add("Connexion")

        # Configurer les onglets
        self.setup_home_tab()
        self.setup_signup_tab()
        self.setup_login_tab()

        # Initialiser le fichier de données des utilisateurs
        self.users_file = 'data/players/users.json'
        if not os.path.isfile(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

    def setup_home_tab(self):
        # Créer le contenu pour l'onglet Accueil
        self.home_tab = self.tabview.tab("Accueil")

        self.welcome_label = ctk.CTkLabel(self.home_tab, text="Bienvenue", font=("Arial", 24))
        self.welcome_label.pack(pady=20)

        if self.current_user:
            self.welcome_label.config(text=f"Bienvenue, {self.current_user['firstname']}")

        # Ajouter un bouton de déconnexion
        self.logout_button = ctk.CTkButton(self.home_tab, text="Se déconnecter", command=self.logout)
        self.logout_button.pack(pady=10)

    def setup_signup_tab(self):
        # Créer le contenu pour l'onglet Inscription
        self.signup_tab = self.tabview.tab("Inscription")

        # Créer un frame pour les informations de l'utilisateur
        self.info_frame = ctk.CTkFrame(self.signup_tab)
        self.info_frame.pack(pady=10, padx=20, fill="x")

        # Nom d'utilisateur
        self.signup_username_entry = ctk.CTkEntry(self.info_frame, placeholder_text="Nom d'utilisateur")
        self.signup_username_entry.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Prénom
        self.signup_firstname_entry = ctk.CTkEntry(self.info_frame, placeholder_text="Prénom")
        self.signup_firstname_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Nom
        self.signup_lastname_entry = ctk.CTkEntry(self.info_frame, placeholder_text="Nom")
        self.signup_lastname_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        # Mot de passe
        self.signup_password_entry = ctk.CTkEntry(self.info_frame, placeholder_text="Mot de passe", show="*")
        self.signup_password_entry.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # Âge
        self.age_entry = ctk.CTkEntry(self.info_frame, placeholder_text="Âge")
        self.age_entry.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # Genre
        self.gender_var = tk.StringVar(value="")

        self.gender_frame = ctk.CTkFrame(self.signup_tab)
        self.gender_frame.pack(pady=5, padx=20)

        self.gender_male_rb = ctk.CTkRadioButton(self.gender_frame, text="Homme", variable=self.gender_var,
                                                 value="Homme", width=70)
        self.gender_male_rb.pack(side="left", padx=10)

        self.gender_female_rb = ctk.CTkRadioButton(self.gender_frame, text="Femme", variable=self.gender_var,
                                                   value="Femme", width=70)
        self.gender_female_rb.pack(side="left", padx=10)

        # Boutons
        self.buttons_frame = ctk.CTkFrame(self.signup_tab)
        self.buttons_frame.pack(pady=10, padx=20, fill="x")

        self.signup_submit_button = ctk.CTkButton(self.buttons_frame, text="S'inscrire", command=self.signup)
        self.signup_submit_button.pack(side="left", padx=10)

    def setup_login_tab(self):
        # Créer le contenu pour l'onglet Connexion
        self.login_tab = self.tabview.tab("Connexion")

        self.login_username_entry = ctk.CTkEntry(self.login_tab, placeholder_text="Nom d'utilisateur")
        self.login_username_entry.pack(pady=10)

        self.login_password_entry = ctk.CTkEntry(self.login_tab, placeholder_text="Mot de passe", show="*")
        self.login_password_entry.pack(pady=10)

        self.login_submit_button = ctk.CTkButton(self.login_tab, text="Se connecter", command=self.login)
        self.login_submit_button.pack(pady=10)

    def open_user_window(self):
        if hasattr(self, 'user_window') and self.user_window.winfo_exists():
            self.user_window.focus()
        else:
            self.withdraw()

            self.user_window = ctk.CTkToplevel(self)
            self.user_window.title("Profil et Jeux")
            self.user_window.geometry("1280x720")

            self.session_start_time = datetime.now()

            self.user_window.protocol("WM_DELETE_WINDOW", self.on_close_user_window)

            profile_frame = ctk.CTkFrame(self.user_window)
            profile_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            games_frame = ctk.CTkFrame(self.user_window)
            games_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

            profile_label = ctk.CTkLabel(profile_frame, text=f"Nom: {self.current_user['lastname']}\n"
                                                             f"Prénom: {self.current_user['firstname']}\n"
                                                             f"Âge: {self.current_user['age']}\n"
                                                             f"Genre: {self.current_user['gender']}",
                                         font=("Arial", 18))
            profile_label.pack(pady=20)

            launch_game_button1 = ctk.CTkButton(games_frame, text=os.listdir("games")[0], command=self.launch_chemin)
            launch_game_button1.pack(pady=10)

            launch_game_button2 = ctk.CTkButton(games_frame, text=os.listdir("games")[1], command=self.launch_calcul)
            launch_game_button2.pack(pady=10)

            launch_game_button3 = ctk.CTkButton(games_frame, text=os.listdir("games")[2], command=self.launch_couleur)
            launch_game_button3.pack(pady=10)

            logout_button = ctk.CTkButton(profile_frame, text="Se déconnecter", command=self.logout)
            logout_button.pack(pady=10)

            # Création du tableau des scores
            self.scores_table = ttk.Treeview(self.user_window, columns=('Jeu', 'Détails'), show='headings')
            self.scores_table.heading('Jeu', text='Jeu')
            self.scores_table.heading('Détails', text='Détails')
            self.scores_table.pack(fill='both', expand=True, pady=20, padx=20)



    def on_close_user_window(self):
        # Sauvegarder les données et générer le PDF lorsque l'utilisateur se déconnecte
        if self.current_user:
            self.generate_pdf_report()
        # Détruire la fenêtre utilisateur et restaurer la fenêtre principale
        self.user_window.destroy()
        self.deiconify()  # Réafficher la fenêtre principale

    def launch_chemin(self):
        try:
            process = subprocess.Popen(['python',f'games/{os.listdir(path)[0]}/main.py',self.current_user['username']])
            # Récupérer les scores et les mettre à jour après la fin du jeu
            process.communicate()  # Attendre la fin du processus
            self.update_path_game_scores()
        except FileNotFoundError as e:
            messagebox.showerror("Erreur", f"Fichier de jeu non trouvé: {e}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")
  

    def update_path_game_scores(self):
    # Simuler la récupération des scores du fichier JSON
        path_game_time = self.read_json_file('data/time_record.json')
        details = f"Time: {int(path_game_time.get('time_elapsed', 0))}, "
        self.update_scores_table("Jeu de Chemin", details)


    def launch_calcul(self):
        try:
            process = subprocess.Popen(['python', f'games/{os.listdir(path)[1]}/main.py', self.current_user['username']])
            # Récupérer les scores et les mettre à jour après la fin du jeu
            process.communicate()  # Attendre la fin du processus
            self.update_calculation_game_scores()
        except FileNotFoundError as e:
            messagebox.showerror("Erreur", f"Fichier de jeu non trouvé: {e}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")

    def update_calculation_game_scores(self):
        # Simuler la récupération des scores du fichier JSON
            calculation_game_data = self.read_json_file('data/math_game_data.json')
            details = f"Correctes: {calculation_game_data.get('total_correct_answers', 0)}, " \
                  f"Erreurs: {', '.join(calculation_game_data.get('incorrect_formulas', []))}"
            self.update_scores_table("Jeu de Calcul", details)

    def launch_couleur(self):
        try:
            process = subprocess.Popen(['python', f'games/{os.listdir(path)[2]}/main.py', self.current_user['username']])
            # Récupérer les scores et les mettre à jour après la fin du jeu
            process.communicate()  # Attendre la fin du processus
            self.update_color_game_scores()
        except FileNotFoundError as e:
            messagebox.showerror("Erreur", f"Fichier de jeu non trouvé: {e}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")

    def update_color_game_scores(self):
        # Simuler la récupération des scores du fichier JSON
        color_game_data = self.read_json_file('data/color_game_data.json')
        details = f"High Score: {color_game_data.get('high_score', 0)}, " 
        self.update_scores_table("Jeu de Couleur", details)


    def update_scores_table(self, game_name, details):

        self.after(5000, self.update_calculation_game_scores)

        self.after(5002, self.update_path_game_scores)
        games = [self.scores_table.item(item)['values'][0] for item in self.scores_table.get_children()]
        self.after(5001, self.update_color_game_scores)
 
        if game_name in games:
            for item in self.scores_table.get_children():
                if self.scores_table.item(item)['values'][0] == game_name:
                    self.scores_table.item(item, values=(game_name, details))
                    break
        else:
        # Sinon, insère un nouveau jeu avec les détails
            self.scores_table.insert('', 'end', values=(game_name, details))


    def signup(self):
        # Récupérer les informations du formulaire
        username = self.signup_username_entry.get()
        firstname = self.signup_firstname_entry.get()
        lastname = self.signup_lastname_entry.get()
        password = self.signup_password_entry.get()
        age = self.age_entry.get()
        gender = self.gender_var.get()

        # Validation des données
        if not all([username, firstname, lastname, password, age, gender]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return

        # Hash du mot de passe
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Charger les utilisateurs existants
        with open(self.users_file, 'r') as f:
            users = json.load(f)

        # Vérifier si l'utilisateur existe déjà
        if username in users:
            messagebox.showerror("Erreur", "Cet utilisateur existe déjà")
            return

        # Ajouter le nouvel utilisateur
        users[username] = {
            'firstname': firstname,
            'lastname': lastname,
            'password': hashed_password,
            'age': age,
            'gender': gender,
            'username': username
        }

        # Sauvegarder dans le fichier JSON
        with open(self.users_file, 'w') as f:
            json.dump(users, f)

        # Message de succès
        messagebox.showinfo("Succès", "Inscription réussie")

    def login(self):
        # Récupérer les informations de connexion
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        # Charger les utilisateurs existants
        with open(self.users_file, 'r') as f:
            users = json.load(f)

        # Vérifier si l'utilisateur existe
        if username not in users:
            messagebox.showerror("Erreur", "Utilisateur non trouvé")
            return

        # Vérifier le mot de passe
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if users[username]['password'] != hashed_password:
            messagebox.showerror("Erreur", "Mot de passe incorrect")
            return

        # Connexion réussie
        self.current_user = users[username]
        messagebox.showinfo("Succès", f"Bienvenue, {self.current_user['firstname']}")
        self.open_user_window()

    def logout(self):
        # Réinitialiser les données utilisateur et revenir à l'écran de connexion
        self.current_user = None
        self.deiconify()  # Réafficher la fenêtre principale
        self.user_window.destroy()

    def on_closing(self):
        # Gestion de la fermeture de la fenêtre principale
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter?"):
            self.destroy()

    
    def read_json_file(self, filename):
        # Lire un fichier JSON et retourner son contenu
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        return {}

    from fpdf import FPDF

# Fonction pour générer le rapport PDF
    def generate_pdf_report(self):
        pdf = FPDF()
        pdf.add_page()
        
        # Titre
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="Rapport des scores", ln=True, align="C")
        
        pdf.ln(10)  # Saut de ligne

        # Informations utilisateur
        pdf.set_font("Arial", size=12)
        if self.current_user:
            pdf.cell(200, 10, txt=f"Utilisateur: {self.current_user['firstname']} {self.current_user['lastname']}", ln=True)
            pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        
        pdf.ln(10)  # Saut de ligne

        # Scores des jeux
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Scores des jeux :", ln=True)

        for item in self.scores_table.get_children():
            game_name, details = self.scores_table.item(item)['values']
            pdf.cell(200, 10, txt=f"{game_name}: {details}", ln=True)

        # Sauvegarder le fichier PDF
        report_name = f"rapport_scores_{self.current_user['username']}.pdf"
        pdf.output(f'data/rapport/{report_name}')
        
        messagebox.showinfo("Rapport généré", f"Le rapport des scores a été enregistré sous le nom {report_name}")

if __name__ == "__main__":
    
    app = MainApp()
    app.mainloop()
