import pygame
from settings import *
from support import import_folder
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.import_assets()

        #animation
        self.status = 'down_idle'

        #movement
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

        #magic
        self.magic_index = 0
        self.magics = list(magic_data.keys())
        self.current_magic = self.magics[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.create_magic = create_magic
        self.magic_info = list(magic_data.values())

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
                self.create_magic(self.current_magic, self.magic_info[self.magic_index]['cost'], 
                                  magic_data[self.current_magic]['strength'] + self.stats['magic'])
        
        #switches
            if keys[pygame.K_s] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.switch_time = pygame.time.get_ticks()
                self.weapon_index += 1
                if self.weapon_index >= len(self.weapons):
                    self.weapon_index = 0
                self.current_weapon = self.weapons[self.weapon_index]

            if keys[pygame.K_f] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                self.magic_index += 1
                if self.magic_index >= len(self.magics):
                    self.magic_index = 0
                self.current_magic = self.magics[self.magic_index]

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
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_cd:
                self.can_switch_magic = True

    def animate(self):
        animation = self.animations[self.status]
        self.frame += self.animation_speed
        if self.frame >= len(animation):
            self.frame = 0
        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)


    def update(self):
        self.input()
        self.update_status()
        self.animate()
        self.cooldowns()
        self.move(self.speed)

