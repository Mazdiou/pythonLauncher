import os
import pygame

pygame.init()

# Vérifier le répertoire de travail actuel
print("Current working directory:", os.getcwd())

# Charger les images des maisons
try:
    houses = [
        pygame.image.load("img/H_yellow.png"),
        pygame.image.load("img/H_red.png"),
        pygame.image.load("img/H_green.png"),
        pygame.image.load("img/H_blue.png")
    ]
except FileNotFoundError as e:
    print("Error loading images:", e)
