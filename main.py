import os
import pygame
from sys import exit
from random import randint, choice

from characters.knight import Knight
from characters.vulture import Vulture

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

vulture_idle = [pygame.image.load(os.path.join(os.path.join("graphics", "vulture"), "Vulture.png")).convert_alpha()]
vulture_death = [
    pygame.image.load(os.path.join(os.path.join("graphics", "vulture"), "Vulture_death.png")).convert_alpha()]
vulture_move = [pygame.transform.smoothscale(x, (int(x.get_width() * 1.2), (x.get_height() * 1.2))) for x in
                get_images_from_folder(os.path.join(os.path.join("graphics", "vulture"), "move"))]
vulture_attack = get_images_from_folder(os.path.join(os.path.join("graphics", "vulture"), "attack"))

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
knight = Knight.create_knight(cloud_1_rect, knight_idle, knight_walk, knight_attack, knight_hurt, knight_death,
                              knight_jump, clouds)
player.add(knight)

enemies = pygame.sprite.Group()

spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 3000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == spawn_timer:
            x, y = choice((-20, SCREEN_WIDTH + 20)), randint(0, SCREEN_HEIGHT // 2)
            vulture = Vulture(x, y, vulture_idle, vulture_move, vulture_attack, vulture_death, knight)
            enemies.add(vulture)

    screen.blit(city_surface, (0, 0))
    screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 0))

    screen.blit(cloud_1, cloud_1_rect)
    screen.blit(cloud_2, cloud_2_rect)
    screen.blit(cloud_1, cloud_3_rect)

    player.draw(screen)
    player.update()

    enemies.draw(screen)
    enemies.update()

    pygame.display.update()
    clock.tick(60)
