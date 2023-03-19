import pygame
from pygame import Rect, key, mouse, transform

from characters.character import Character


class Knight(Character):
    GRAVITY_VELOCITY = 1
    MOVEMENT_VELOCITY = 4

    def __init__(self, x, y, idle, walk, attack, hurt, death, jump, clouds: list):
        super().__init__(x, y, idle, walk, attack, death)
        self.rect: Rect = self.image.get_rect(midbottom=(x, y)).inflate(0, -4)
        self.jump_image = jump
        self.hurt_images = hurt
        self.clouds = clouds
        self.gravity = 0
        self.colliding = False
        self.going_right = True
        self.moved = False
        self.attacking = False
        self.attack_timer = 0

    @classmethod
    def create_knight(cls, cloud_coordinates: Rect, idle, walk, attack, hurt, death, jump: pygame.image, clouds: list):
        x, y = cloud_coordinates.x + cloud_coordinates.width // 2, cloud_coordinates.top
        return cls(x, y, idle, walk, attack, hurt, death, jump, clouds)

    @property
    def coordinates(self):
        return self.rect.x, self.rect.y

    def movement(self):
        keys = key.get_pressed()
        if any((keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_SPACE] and self.colliding)):
            if keys[pygame.K_a]:
                self.rect.x -= self.MOVEMENT_VELOCITY
                self.going_right = False
                if self.colliding:
                    self.image, self.walk_index = self.animation(self.going_right, self.walk_images, self.walk_index)
                else:
                    self.image, self.walk_index = transform.flip(self.jump_image, True, False), self.walk_index
            if keys[pygame.K_d]:
                self.rect.x += self.MOVEMENT_VELOCITY
                self.going_right = True
                if self.colliding:
                    self.image, self.walk_index = self.animation(self.going_right, self.walk_images, self.walk_index)
                else:
                    self.image, self.walk_index = self.jump_image, self.walk_index
            if keys[pygame.K_SPACE] and self.colliding:
                self.gravity = -17
                self.image = self.jump_image if self.going_right else transform.flip(self.jump_image, True, False)
            self.moved = True

    def attack(self):
        keys = key.get_pressed()

        if (keys[pygame.K_f] or mouse.get_pressed()[0]) and self.attack_timer == 0:
            self.attack_timer = 60
            self.attacking = True

        if self.attacking:
            self.image, self.attack_index = self.animation(self.going_right, self.attack_images, self.attack_index,
                                                           0.15)
            if self.attack_index + 0.15 >= len(self.attack_images):
                self.attacking = False

        if self.attack_timer > 0:
            self.attack_timer -= 1

    def apply_gravity(self):
        self.gravity += self.GRAVITY_VELOCITY
        self.rect.y += self.gravity
        self.collision()

    def collision(self):
        for cloud in self.clouds:
            if self.rect.colliderect(cloud) and self.rect.bottomright[0] - self.rect.width // 2 > cloud.topleft[0]:
                self.rect.midbottom = (self.rect.midbottom[0], cloud.midtop[1])
                self.gravity = 0
                self.colliding = True
                break
        else:
            self.colliding = False

    def update(self):
        self.movement()
        self.attack()
        self.apply_gravity()
        if not self.moved and not self.attacking:
            self.image, self.idle_index = self.animation(self.going_right, self.idle_images, self.idle_index, 0.03)
        self.moved = False if self.colliding else True
