import pygame
from pygame import sprite, Rect, key


class Character(sprite.Sprite):

    def __init__(self, x: int, y: int, idle_images: list, walk_images: list, attack_images: list, hurt_images: list,
                 death_images: list):
        super().__init__()
        self.x = x
        self.y = y
        self.idle_images = idle_images
        self.walk_images = walk_images
        self.attack_images = attack_images
        self.hurt_images = hurt_images
        self.death_images = death_images
        self.image = idle_images[0]
        self.rect: Rect = self.image.get_rect(midbottom=(x, y))
        self.gravity = 0


class Knight(Character):
    GRAVITY_VELOCITY = 1
    MOVEMENT_VELOCITY = 4

    def __init__(self, x, y, idle, walk, attack, hurt, death, jump, clouds: list):
        super().__init__(x, y, idle, walk, attack, hurt, death)
        self.jump_images = jump
        self.clouds = clouds

    @classmethod
    def create_knight(cls, cloud_coordinates: Rect, idle, walk, attack, hurt, death, jump, clouds: list):
        x, y = cloud_coordinates.x + cloud_coordinates.width // 2, cloud_coordinates.top
        return cls(x, y, idle, walk, attack, hurt, death, jump, clouds)

    def movement(self):
        keys = key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.MOVEMENT_VELOCITY
        if keys[pygame.K_d]:
            self.rect.x += self.MOVEMENT_VELOCITY
        if keys[pygame.K_SPACE]:
            self.gravity = -15

    def apply_gravity(self):
        self.gravity += self.GRAVITY_VELOCITY
        self.rect.y += self.gravity
        self.collision()

    def collision(self):
        for cloud in self.clouds:
            if self.rect.colliderect(cloud) and self.rect.bottomright[0] > cloud.topleft[0] + 20:
                self.rect.midbottom = (self.rect.midbottom[0], cloud.midtop[1])
                self.gravity = 0
                break

    def update(self):
        self.movement()
        self.apply_gravity()
