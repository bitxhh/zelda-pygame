import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade_Menu


class Level:
    def __init__(self):
        self.displey_surface = pygame.display.get_surface()
        self.paused = False
        self.restart = False
        self.all_sprites = pygame.sprite.Group()

        # setup sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # weapon
        self.current_attack = None
        self.attackable_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        # map setup
        self.create_map()

        # UI
        self.ui = UI()

        # particles
        self.animation_player = AnimationPlayer()
        self.magic = MagicPlayer(self.animation_player)

        #upgrade-menu
        self.upgrade_menu = Upgrade_Menu(self.player)

        #sounds
        self.hit = pygame.mixer.Sound('audio/Hit.wav')
        main_sound = pygame.mixer.Sound('audio/main.mp3')
        main_sound.play(loops=-1)

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_Objects.csv'),
            'entities': import_csv_layout('map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('graphics/Grass'),
            'objects': import_dict('graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                'grass',
                                random_grass_image)

                        if style == 'object':
                            surf = graphics['objects'][col]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x, y), [self.visible_sprites],
                                                     self.obstacle_sprites, self.create_attack,
                                                     self.destroy_attack, self.create_magic,
                                                     self.reset)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites, self.damage_player, self.trigger_animation, self.add_xp)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, cost, strength):
        if style == 'heal':
            self.magic.heal(self.player, self.player.rect.center, cost, strength, [self.visible_sprites])
        if style == 'flame':
            self.magic.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    def add_xp(self, amount):
        self.player.exp += amount
    def toggle_menu(self):
        self.paused = not self.paused
    def trigger_animation(self, pos, particle_type, sprite_type):
        self.animation_player.create_particles(particle_type, pos, sprite_type, [self.visible_sprites])
    def damage_player(self, amount, attack_type):
        if not self.player.attacked:
            self.hit.play()
            self.player.hp -= amount
            self.player.attacked = True
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center,  'damage', [self.visible_sprites])
    def player_attack_logic(self):
        if self.attack_sprites:
            for sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(target_sprite.rect.center, 'grass_particles', [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, sprite.sprite_type)
                            target_sprite.attacked = True
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.displey(self.player, self.paused)
        if self.paused:
            self.upgrade_menu.display(self.player)
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
    def reset(self):
        for sprite in self.visible_sprites:
            sprite.kill()
        for sprite in self.attackable_sprites:
            sprite.kill()
        for sprite in self.obstacle_sprites:
            sprite.kill()
        del self.player
        self.create_map()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displey_surface = pygame.display.get_surface()
        self.half_width = self.displey_surface.get_size()[0] // 2
        self.half_height = self.displey_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        # floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.displey_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.displey_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)
