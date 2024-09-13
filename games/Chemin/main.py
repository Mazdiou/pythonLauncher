import pygame
import sys
import random
from maze import Maze
from player import Player
from clock import Clock
from game import Game
import json

pygame.init()
pygame.font.init()

path = "games\Chemin"

# Charger les images des maisons
houses = [
    pygame.image.load(f'{path}\img\H_yelloww.png'),
    pygame.image.load(f'{path}\img\H_red.png'),
    pygame.image.load(f'{path}\img\H_green.png'),
    pygame.image.load(f'{path}\img\H_blue.png')
]

# Redimensionner les images des maisons pour qu'elles s'adaptent au labyrinthe
tile_size = 30  # Assurez-vous que cela correspond à la taille des tuiles dans votre labyrinthe
houses = [pygame.transform.scale(house, (tile_size, tile_size)) for house in houses]

# Choisir une maison au hasard pour commencer
current_house_image = random.choice(houses)

class Session:
    def __init__(self, joueur_id):
        self.joueur_id = joueur_id
        self.jeux_joues = []

    def ajouter_jeu(self, nom_jeu, donnees_jeu):
        self.jeux_joues.append({
            "nom_jeu": nom_jeu,
            "donnees_jeu": donnees_jeu
        })

    def sauvegarder_donnees(self):
        # Sauvegarder les données de la session dans un fichier JSON
        with open(f"session_{self.joueur_id}.json", 'w') as f:
            json.dump(self.jeux_joues, f, indent=4)

class Main:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 30)
        self.message_color = pygame.Color("cyan")
        self.running = True
        self.FPS = pygame.time.Clock()
        self.clock = Clock()  # Ajouter l'instance de Clock ici

    def instructions(self):
        instructions1 = self.font.render('Use', True, self.message_color)
        instructions2 = self.font.render('Arrow Keys', True, self.message_color)
        instructions3 = self.font.render('to Move', True, self.message_color)
        self.screen.blit(instructions1, (655, 300))
        self.screen.blit(instructions2, (610, 331))
        self.screen.blit(instructions3, (630, 362))

    def _draw(self, maze, tile, player, game, clock):
        # Dessiner le labyrinthe
        for cell in maze.grid_cells:
            cell.draw(self.screen, tile)

        # Dessiner le joueur
        player.draw(self.screen)
        player.update()

        # Ajouter le point final avec l'image de la maison actuelle
        self.screen.blit(current_house_image, (maze.grid_cells[-1].x * tile, maze.grid_cells[-1].y * tile))

        # Instructions, horloge, message de victoire
        self.instructions()
        if game.is_game_over(player):
            self.clock.stop_timer()  # Arrêter le chronomètre
            self.screen.blit(game.message(), (610, 120))
        else:
            self.clock.update_timer()  # Mettre à jour le chronomètre
        self.screen.blit(self.clock.display_timer(), (625, 200))

        pygame.display.flip()


    def save_time(self, time_elapsed):
        data = {
            "time_elapsed" : time_elapsed
        }
        with open("data/time_record.json", "w") as file:
            json.dump(data, file)

    def handle_end_menu(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.display_end_menu()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return 'replay'
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def display_end_menu(self):
        self.screen.fill((0, 0, 0))
        end_font = pygame.font.SysFont("impact", 50)
        draw_text('Bravo', end_font, (0, 0, 255), self.screen, self.screen.get_width() // 2, 150)
        draw_text('Appuie sur R pour recommencer', self.font, (255, 255, 255), self.screen, self.screen.get_width() // 2, 250)
        draw_text('Appuie sur Q pour quitter', self.font, (255, 255, 255), self.screen, self.screen.get_width() // 2, 350)

    def main(self, frame_size, tile):
        while self.running:
            cols, rows = frame_size[0] // tile, frame_size[-1] // tile
            maze = Maze(cols, rows)
            game_instance = Game(maze.grid_cells[-1], tile)
            player = Player(tile // 3, tile // 3)
            self.clock.start_timer()  # Démarrer le chronomètre
            maze.generate_maze()

            game_over = False
            result = None  # Initialisation de la variable result

            while not game_over:
                self.screen.fill("gray")
                self.screen.fill(pygame.Color("darkslategray"), (603, 0, 752, 752))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            player.left_pressed = True
                        if event.key == pygame.K_RIGHT:
                            player.right_pressed = True
                        if event.key == pygame.K_UP:
                            player.up_pressed = True
                        if event.key == pygame.K_DOWN:
                            player.down_pressed = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            player.left_pressed = False
                        if event.key == pygame.K_RIGHT:
                            player.right_pressed = False
                        if event.key == pygame.K_UP:
                            player.up_pressed = False
                        if event.key == pygame.K_DOWN:
                            player.down_pressed = False

                player.check_move(tile, maze.grid_cells, maze.thickness)

                if game_instance.is_game_over(player):
                    game_over = True
                    player.left_pressed = False
                    player.right_pressed = False
                    player.up_pressed = False
                    player.down_pressed = False

                    # Replacer le joueur au début du labyrinthe
                    player.x, player.y = tile // 3, tile // 3

                    # Choisir une nouvelle maison pour le prochain niveau
                    global current_house_image
                    current_house_image = random.choice(houses)

                    # Sauvegarder le temps écoulé
                    time_elapsed = self.clock.elapsed_time
                    self.save_time(time_elapsed)

                    # Afficher le menu de fin de partie et gérer le choix de l'utilisateur
                    result = self.handle_end_menu()
                    if result == 'replay':
                        break  # Sortir de la boucle actuelle pour relancer le jeu

                self._draw(maze, tile, player, game_instance, self.clock)
                self.FPS.tick(60)

            if result != 'replay':
                break  # Quitter le jeu si l'utilisateur choisit de ne pas rejouer

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

if __name__ == "__main__":
    window_size = (602, 602)
    screen_dimensions = (window_size[0] + 150, window_size[-1])
    tile_size = 30
    screen_instance = pygame.display.set_mode(screen_dimensions)
    pygame.display.set_caption("Maze")

    maze_game = Main(screen_instance)
    maze_game.main(window_size, tile_size)
