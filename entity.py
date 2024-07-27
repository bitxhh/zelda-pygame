import pygame
from settings import *
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.animation_speed = 0.15
        self.frame = 0
        self.direction = pygame.math.Vector2()
        self.steps = pygame.mixer.Sound('audio/steps.mp3')
        self.steps.set_volume(0.2)
        self.can_step = True
        self.step_time = None

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
            if self.can_step:
                self.steps.play()
                self.can_step = False
                self.step_time = pygame.time.get_ticks()
        self.hitbox.x += self.direction.x * speed
        self.colission('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.colission('vertical')
        self.rect.center = self.hitbox.center

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
