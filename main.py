import os

import pygame
from sys import exit

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 450
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SkyKnight")
clock = pygame.time.Clock()
font = pygame.font.Font(os.path.join("font", "pixChicago.ttf"), 20)

city_surface = pygame.image.load(os.path.join(os.path.join("graphics", "background"), "background.png")).convert()
text_surface = font.render("Score", False, "Black")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(city_surface, (0, 0))
    screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 0))

    pygame.display.update()
    clock.tick(60)
