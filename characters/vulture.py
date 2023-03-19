import math

from pygame import Rect, transform

from characters.character import Character
from characters.knight import Knight


class Vulture(Character):

    def __init__(self, x, y, idle, walk, attack, death, knight: Knight):
        super().__init__(x, y, idle, walk, attack, death)
        self.rect: Rect = self.image.get_rect(midbottom=(x, y)).inflate(0, -20)
        self.going_right = True if x < 0 else False
        self.knight = knight

    def move(self):
        player_x, player_y = self.knight.coordinates

        if self.rect.x < player_x:
            self.rect.x += 2
            self.going_right = False
        elif self.rect.x > player_x:
            self.rect.x -= 2
            self.going_right = True

        if self.rect.y < player_y:
            self.rect.y += 2
        elif self.rect.y > player_y:
            self.rect.y -= 2

        dx = player_x - self.rect.x
        dy = player_y - self.rect.y

        angle = math.atan2(dy, dx) if not self.going_right else math.atan2(dy, dx) + 160

        self.image = transform.rotate(self.image, math.degrees(-angle))

    def animate_movement(self):
        self.image, self.walk_index = self.animation(self.going_right, self.walk_images, self.walk_index)

    def update(self):
        self.animate_movement()
        self.move()
