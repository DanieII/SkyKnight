import pygame
from pygame import sprite, Rect, key, transform


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
        self.rect: Rect = self.image.get_rect(midbottom=(x, y)).inflate(0, -4)
        self.idle_index = 0
        self.walk_index = 0
        self.attack_index = 0
        self.hurt_index = 0

    @staticmethod
    def animation(direction, images, index, speed=0.1):
        index += speed
        if index > len(images):
            index = 0

        if direction:
            return images[int(index)], index

        return transform.flip(images[int(index)], True, False), index


class Knight(Character):
    GRAVITY_VELOCITY = 1
    MOVEMENT_VELOCITY = 4

    def __init__(self, x, y, idle, walk, attack, hurt, death, jump, clouds: list):
        super().__init__(x, y, idle, walk, attack, hurt, death)
        self.jump_image = jump
        self.clouds = clouds
        self.gravity = 0
        self.colliding = False
        self.going_right = True
        self.moved = False

    @classmethod
    def create_knight(cls, cloud_coordinates: Rect, idle, walk, attack, hurt, death, jump: pygame.image, clouds: list):
        x, y = cloud_coordinates.x + cloud_coordinates.width // 2, cloud_coordinates.top
        return cls(x, y, idle, walk, attack, hurt, death, jump, clouds)

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
        self.apply_gravity()
        if not self.moved:
            self.image, self.idle_index = self.animation(self.going_right, self.idle_images, self.idle_index, 0.03)
        self.moved = False if self.colliding else True
