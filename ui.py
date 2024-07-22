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

    def selection_box(self, top, left, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.displey_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.displey_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.displey_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=(self.exp_x - 20, self.exp_y - 20))
        pygame.draw.rect(self.displey_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.displey_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.displey_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def weapon_overlay(self, current_weapon, has_switched):
        bg_rect = self.selection_box(630, 10, has_switched)
        weapon_surf = pygame.image.load(current_weapon['graphic']).convert_alpha()
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.displey_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, current_magic, has_switched):
        bg_rect = self.selection_box(635, 80, has_switched)
        magic_surf = weapon_surf = pygame.image.load(current_magic['graphic']).convert_alpha()
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.displey_surface.blit(magic_surf, magic_rect)

    def displey(self, player):
        self.show_bar(player.hp, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_exp(player.exp)
        self.weapon_overlay(weapon_data[player.current_weapon], not player.can_switch_weapon)
        self.magic_overlay(magic_data[player.current_magic], not player.can_switch_magic)