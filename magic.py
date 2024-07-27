import pygame
from settings import *
from random import randint


class MagicPlayer:
    def __init__(self, particles_player):
        self.particles_player = particles_player
        self.direction = pygame.math.Vector2()
        self.sounds = {
            'heal': pygame.mixer.Sound('audio/heal.wav')
        }

    def heal(self, player, pos, cost, strength, groups):
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.hp += strength
            player.energy -= cost
            if player.hp >= player.stats['health']:
                player.hp = player.stats['health']
            self.particles_player.create_particles('aura', pos, 'magic', groups)
            self.particles_player.create_particles('heal', pos + pygame.math.Vector2(0, -45), 'magic', groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            if '_idle' in player.status:
                if player.status == 'right_idle': self.direction = pygame.math.Vector2(1, 0)
                if player.status == 'left_idle': self.direction = pygame.math.Vector2(-1, 0)
                if player.status == 'up_idle': self.direction = pygame.math.Vector2(0, -1)
                if player.status == 'down_idle': self.direction = pygame.math.Vector2(0, 1)
            else:
                self.direction = player.direction

            for i in range(1, 4):
                offset = self.direction * i * TILESIZE + pygame.math.Vector2(randint(-TILESIZE // 3, TILESIZE // 3),
                                                                               randint(-TILESIZE // 3, TILESIZE // 3))
                self.particles_player.create_particles('flame',
                                                       player.rect.center + offset,
                                                       'magic',
                                                       groups)
