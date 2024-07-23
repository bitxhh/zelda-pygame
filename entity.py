import pygame
from settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.animation_speed = 0.15
        self.frame = 0
        self.direction = pygame.math.Vector2()

    def colission(self, direction):
     if direction == 'horizontal':
        for sprite in self.obstacles:
            if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.x > 0:
                    self.hitbox.right = sprite.hitbox.left
                if self.direction.x < 0:
                    self.hitbox.left = sprite.hitbox.right
     if direction == 'vertical':
         for sprite in self.obstacles:
             if sprite.hitbox.colliderect(self.hitbox):
                if self.direction.y > 0:
                    self.hitbox.bottom = sprite.hitbox.top
                if self.direction.y < 0:
                    self.hitbox.top = sprite.hitbox.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.colission('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.colission('vertical')
        self.rect.center = self.hitbox.center