from sprites import *
import random
import json
import pygame

class Game:
    def __init__(self, player_username):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jeux de couleur")
        self.clock = pygame.time.Clock()
        self.flash_colours = [YELLOW, BLUE, RED, GREEN]
        self.colours = [DARKYELLOW, DARKBLUE, DARKRED, DARKGREEN]
        self.buttons = [
            Button(110, 50, DARKYELLOW),
            Button(330, 50, DARKBLUE),
            Button(110, 270, DARKRED),
            Button(330, 270, DARKGREEN),
        ]
        self.playing = True
        self.score = 0
        self.errors_by_color = {color: 0 for color in self.colours}
        self.high_score = 0
        self.waiting_input = False
        self.current_step = 0
        self.clicked_button = None
        self.pattern = []

        # Initialisation de l'attribut player_username
        self.player_username = player_username
        self.load_data()

    @staticmethod
    def get_high_score():
        try:
            with open("data/color_game_data.json", "r") as file:
                data = json.load(file)
                return data.get("high_score", 0)
        except FileNotFoundError:
            return 0

    def save_data(self):
        try:
            with open("data/color_game_data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        # Sauvegarder les scores du joueur actuel
        data = {
            "high_score": self.high_score,
            "number_of_attempts": self.score,
            "errors_by_color": {str(color): count for color, count in self.errors_by_color.items()}
        }

        with open("data/color_game_data.json", "w") as file:
            json.dump(data, file)

        print(data)

    def load_data(self):
        try:
            with open("data/color_game_data.json", "r") as file:
                data = json.load(file)
                player_data = data.get(self.player_username, {})
                self.high_score = player_data.get("high_score", 0)
                self.errors_by_color = player_data.get("errors_by_color", {color: 0 for color in self.colours})
        except FileNotFoundError:
            self.high_score = 0
            self.errors_by_color = {color: 0 for color in self.colours}

    def new(self):
        self.waiting_input = False
        self.pattern = []
        self.current_step = 0
        self.score = 0
        self.load_data()

    def save_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.save_data()

    def update(self):
        if not self.waiting_input:
            pygame.time.wait(1000)
            self.pattern.append(random.choice(self.colours))
            for button in self.pattern:
                self.button_animation(button)
                pygame.time.wait(200)
            self.waiting_input = True

        else:
            if self.clicked_button and self.clicked_button == self.pattern[self.current_step]:
                self.button_animation(self.clicked_button)
                self.current_step += 1

                if self.current_step == len(self.pattern):
                    self.score += 1
                    self.waiting_input = False
                    self.current_step = 0

            elif self.clicked_button and self.clicked_button != self.pattern[self.current_step]:
                self.errors_by_color[self.clicked_button] += 1
                self.game_over_animation()
                self.save_score()
                self.save_data()
                self.playing = False

    def button_animation(self, colour):
        flash_colour = None
        button = None
        for i in range(len(self.colours)):
            if self.colours[i] == colour:
                flash_colour = self.flash_colours[i]
                button = self.buttons[i]

        if flash_colour is not None and button is not None:
            original_surface = self.screen.copy()
            flash_surface = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE))
            flash_surface = flash_surface.convert_alpha()
            r, g, b = flash_colour
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, ANIMATION_SPEED * step):
                    self.screen.blit(original_surface, (0, 0))
                    flash_surface.fill((r, g, b, alpha))
                    self.screen.blit(flash_surface, (button.x, button.y))
                    pygame.display.update()
                    self.clock.tick(FPS)
            self.screen.blit(original_surface, (0, 0))

    def game_over_animation(self):
        original_surface = self.screen.copy()
        flash_surface = pygame.Surface((self.screen.get_size()))
        flash_surface = flash_surface.convert_alpha()
        r, g, b = WHITE
        for _ in range(3):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, ANIMATION_SPEED * step):
                    self.screen.blit(original_surface, (0, 0))
                    flash_surface.fill((r, g, b, alpha))
                    self.screen.blit(flash_surface, (0, 0))
                    pygame.display.update()
                    self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(BGCOLOUR)
        UIElement(170, 20, f"Score: {str(self.score)}").draw(self.screen)
        UIElement(370, 20, f"High score: {str(self.high_score)}").draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.clicked(mouse_x, mouse_y):
                        self.clicked_button = button.colour

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.clicked_button = None
            self.events()
            self.draw()
            self.update()



game = Game("")
while True:
    game.new()
    game.run()
