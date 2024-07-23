import pygame
from settings import *

class UI:
    def __init__(self):
        
        #general
        self.displey_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        self.exp_x, self.exp_y = self.displey_surface.get_size()

        #image_pathes
        self.overlay_data = [[], []]
        for key in weapon_data.keys():
            self.overlay_data[0].append(weapon_data[key]['graphic'])
        for key in magic_data.keys():
            self.overlay_data[1].append(magic_data[key]['graphic'])

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.displey_surface, UI_BG_COLOR, bg_rect)

        #converting
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        #show
        pygame.draw.rect(self.displey_surface, color, current_rect)
        pygame.draw.rect(self.displey_surface, UI_BORDER_COLOR, bg_rect, 3)

    def selection_box(self, top, left, current, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.displey_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.displey_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.displey_surface, UI_BORDER_COLOR, bg_rect, 3)
        weapon_surf = pygame.image.load(current).convert_alpha()
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.displey_surface.blit(weapon_surf, weapon_rect)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=(self.exp_x - 20, self.exp_y - 20))
        pygame.draw.rect(self.displey_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.displey_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.displey_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def displey(self, player):
        self.show_bar(player.hp, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_exp(player.exp)
        self.selection_box(630, 10, self.overlay_data[0][player.weapon_index], not player.can_switch_weapon)
        self.selection_box(635, 80, self.overlay_data[1][player.magic_index], not player.can_switch_magic)