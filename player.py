import pygame
from settings import *
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.import_assets()

        #animation
        self.status = 'down_idle'
        self.animation_speed = 0.15
        self.frame = 0

        #movement
        self.direction = pygame.math.Vector2()
        self.hitbox = self.rect.inflate((0, -26))

        #weapon
        self.attacking = False
        self.attacking_cd = 400
        self.attack_time = None
        self.create_attack = create_attack
        self.destyor_attack = destroy_attack
        self.weapon_index = 0
        self.weapons = list(weapon_data.keys())
        self.current_weapon = self.weapons[self.weapon_index]
        self.can_switch_weapon = True
        self.switch_time = None
        self.switch_cd = 200

        #stats
        self.stats = {'health': 100, 'energy': 60, 'speed': 5, 'magic': 4, 'attack': 10 }
        self.hp = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.exp = 123

        self.obstacles = obstacle_sprites

    def import_assets(self):
        path = 'graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()
        #movement
        if not self.attacking:
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

        #attacking
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
        #magic
            if keys[pygame.K_m]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print(f'ss')
            if keys[pygame.K_s] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.switch_time = pygame.time.get_ticks()
                self.weapon_index += 1
                if self.weapon_index >= len(self.weapons):
                    self.weapon_index = 0
                self.current_weapon = self.weapons[self.weapon_index]

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.colission('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.colission('vertical')
        self.rect.center = self.hitbox.center

    def update_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            self.status = self.status.split('_')[0] + '_attack'

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attacking_cd:
                self.attacking = False
                self.destyor_attack()
        if not self.can_switch_weapon:
            if current_time - self.switch_time >= self.switch_cd:
                self.can_switch_weapon = True

    def animate(self):
        animation = self.animations[self.status]
        self.frame += self.animation_speed
        if self.frame >= len(animation):
            self.frame = 0
        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

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

    def update(self):
        self.input()
        self.update_status()
        self.animate()
        self.cooldowns()
        self.move(self.speed)

