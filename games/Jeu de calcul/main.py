import customtkinter as ctk
import random
import json



# Configuration de l'interface customtkinter
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class MathGameApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre principale
        self.title("Math Game")
        self.geometry("400x300")

        # Variables de jeu
        self.level = 1
        self.score = 0
        self.current_formula = ""
        self.correct_answer = 0
        self.consecutive_correct_answers = 0
        self.max_consecutive_correct = 0
        self.incorrect_formulas = []

        # Widgets
        self.label_formula = ctk.CTkLabel(self, text="Cliquez sur 'Start' pour commencer", font=("Arial", 20))
        self.label_formula.pack(pady=20)

        self.entry_answer = ctk.CTkEntry(self, placeholder_text="Entrez votre réponse ici")
        self.entry_answer.pack(pady=10)

        self.button_check = ctk.CTkButton(self, text="Vérifier", command=self.check_answer)
        self.button_check.pack(pady=10)

        self.label_result = ctk.CTkLabel(self, text="")
        self.label_result.pack(pady=10)

        self.button_start = ctk.CTkButton(self, text="Start", command=self.start_game)
        self.button_start.pack(pady=10)

        # Bind the closing event to save_data
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def generate_formula(self):
        if self.level <= 3:
            operations = ['+']
        elif self.level <= 6:
            operations = ['-']
        elif self.level <= 9:
            operations = ['+', '-']
        elif self.level <= 12:
            operations = ['*']
        else:
            operations = ['/', '*', '+', '-']

        num_operands = 2 if self.level <= 3 else 2 + (self.level - 3) // 3

        formula = str(random.randint(1, 10))
        for _ in range(num_operands - 1):
            operation = random.choice(operations)
            operand = str(random.randint(1, 10))
            if operation == '/' and operand == '0':
                operand = '1'  # Evite la division par zéro
            formula += f" {operation} {operand}"

        return formula

    def start_game(self):
        self.level = 1
        self.score = 0
        self.consecutive_correct_answers = 0
        self.max_consecutive_correct = 0
        self.incorrect_formulas = []
        self.label_result.configure(text="")
        self.next_formula()

    def next_formula(self):
        self.current_formula = self.generate_formula()
        self.correct_answer = round(eval(self.current_formula), 2)  # Calcul de la réponse correcte
        self.label_formula.configure(text=self.current_formula)
        self.entry_answer.delete(0, ctk.END)

    def check_answer(self):
        try:
            user_answer = float(self.entry_answer.get())
            if user_answer == self.correct_answer:
                self.score += 1
                self.consecutive_correct_answers += 1
                self.max_consecutive_correct = max(self.max_consecutive_correct, self.consecutive_correct_answers)
                self.level += 1
                self.label_result.configure(text="Correct! Niveau suivant.", fg_color="green")
            else:
                self.incorrect_formulas.append(self.current_formula)
                self.consecutive_correct_answers = 0
                self.label_result.configure(text=f"Faux! La réponse correcte était {self.correct_answer}.", fg_color="red")

            self.next_formula()
        except ValueError:
            self.label_result.configure(text="Veuillez entrer un nombre valide.", fg_color="yellow")

    def save_data(self):
        data = {
            "total_correct_answers": self.score,
            "incorrect_formulas": self.incorrect_formulas,
            "max_consecutive_correct_answers": self.max_consecutive_correct
        }
        with open("data/math_game_data.json", "w") as file:
            json.dump(data, file)

    def on_closing(self):
        self.save_data()
        self.destroy()  # Fermer l'application correctement

if __name__ == "__main__":
    app = MathGameApp()
    app.mainloop()
