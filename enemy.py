from entity import Entity
from settings import *
from support import *


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_animation, add_xp):
        super().__init__(groups)
        self.animations = None
        self.sprite_type = 'enemy'
        self.add_xp = add_xp

        # graphic setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame]
        self.trigger_animation = trigger_animation

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacles = obstacle_sprites
        self.can_step = False

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        self.attacked = False
        self.attacked_time = None
        self.death_sound = pygame.mixer.Sound('audio/death.mp3')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])

        # cooldown
        self.damage_player = damage_player
        self.can_attack = True
        self.attack_time = None
        self.attack_cd = 1000

    def import_graphics(self, name):
        path = f'graphics/monsters/{name}/'
        self.animations = {'idle': [], 'move': [], 'attack': []}

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def get_damage(self, player, attack_type):
        if not self.attacked:
            self.attacked_time = pygame.time.get_ticks()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= weapon_data[player.current_weapon]['damage'] + player.stats['attack']
            else:
                self.health -= magic_data[player.current_magic]['strength'] + player.stats['magic']

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_animation(self.rect.center, self.monster_name, self.monster_name)
            self.add_xp(self.exp)
            self.death_sound.play()

    def hit_reaction(self):
        if self.attacked:
            self.direction *= -self.resistance
    def cooldown(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cd:
                self.can_attack = True
        if self.attacked:
            current_time = pygame.time.get_ticks()
            if current_time - self.attacked_time >= 400:
                self.attacked = False

    def animate(self):
        animation = self.animations[self.status]
        self.frame += self.animation_speed
        if self.frame >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
                self.attack_time = pygame.time.get_ticks()
            self.frame = 0
        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        if self.attacked:
            self.image.set_alpha(self.wave_value())
        else:
            self.image.set_alpha(255)

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)

