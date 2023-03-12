import os
import pygame
from sys import exit
from random import randint

from characters import Knight

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SkyKnight")
clock = pygame.time.Clock()
font = pygame.font.Font(os.path.join("font", "pixChicago.ttf"), 20)

city_surface = pygame.image.load(os.path.join(os.path.join("graphics", "background"), "background.png")).convert()
city_surface = pygame.transform.scale(city_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
text_surface = font.render("Score", False, "Black")


def get_images_from_folder(folder):
    all_images = [os.path.join(folder, f) for f in os.listdir(folder)]
    return [pygame.image.load(x).convert_alpha() for x in all_images]


# characters images
knight_idle = get_images_from_folder(os.path.join(os.path.join("graphics", "KnightActions"), "idle"))
knight_walk = get_images_from_folder(os.path.join(os.path.join("graphics", "KnightActions"), "walk"))
knight_attack = get_images_from_folder(os.path.join(os.path.join("graphics", "KnightActions"), "attack"))
knight_hurt = get_images_from_folder(os.path.join(os.path.join("graphics", "KnightActions"), "hurt"))
knight_death = get_images_from_folder(os.path.join(os.path.join("graphics", "KnightActions"), "dead"))
knight_jump = pygame.image.load(os.path.join(os.path.join("graphics", "KnightActions"), "jump.png")).convert_alpha()

# clods y coordinates
first_y, second_y, third_y = [randint(300, 400) for _ in range(3)]

# clouds surfaces with rectangles
cloud_1 = pygame.image.load(os.path.join("graphics", "cloud_1.png")).convert_alpha()
cloud_1 = pygame.transform.scale(cloud_1, (cloud_1.get_width() * 4, cloud_1.get_height() * 4))
cloud_1_rect = cloud_1.get_rect(midleft=(100, first_y))
cloud_1_rect = cloud_1_rect.inflate(-20, -(cloud_1_rect.height - 1))
cloud_3_rect = cloud_1.get_rect(midright=(SCREEN_WIDTH - 100, third_y))
cloud_3_rect = cloud_3_rect.inflate(-20, -(cloud_3_rect.height - 1))

cloud_2 = pygame.image.load(os.path.join("graphics", "cloud_2.png")).convert_alpha()
cloud_2 = pygame.transform.scale(cloud_2, (cloud_2.get_width() * 5, cloud_2.get_height() * 5))
cloud_2_rect = cloud_2.get_rect(center=(SCREEN_WIDTH // 2, second_y))
cloud_2_rect = cloud_2_rect.inflate(-20, -(cloud_2_rect.height - 1))

clouds = [cloud_1_rect, cloud_2_rect, cloud_3_rect]

# groups
player = pygame.sprite.GroupSingle()
player.add(Knight.create_knight(cloud_1_rect, knight_idle, knight_walk, knight_attack, knight_hurt, knight_death,
                                knight_jump, clouds))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(city_surface, (0, 0))
    screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 0))

    screen.blit(cloud_1, cloud_1_rect)
    screen.blit(cloud_2, cloud_2_rect)
    screen.blit(cloud_1, cloud_3_rect)

    player.draw(screen)
    player.update()

    pygame.display.update()
    clock.tick(60)
