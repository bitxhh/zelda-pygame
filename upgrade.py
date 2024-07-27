import pygame
from settings import *


class Upgrade_Menu:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.max_values = list(self.player.max_stats.values())

        # dimensions
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

        # selection
        self.selection_index = 0
        self.can_move = True
        self.move_time = None

    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_RIGHT]:
                if self.selection_index < self.attribute_number - 1:
                    self.selection_index += 1
                else:
                    self.selection_index = 0
                self.can_move = False
                self.move_time = pygame.time.get_ticks()

            if keys[pygame.K_LEFT]:
                if self.selection_index > 0:
                    self.selection_index -= 1
                else:
                    self.selection_index = self.attribute_number - 1
                self.can_move = False
                self.move_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.move_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.move_time >= 300:
                self.can_move = True

    def create_items(self):
        self.item_list = []
        # pos
        for item, index in enumerate(range(self.attribute_number)):
            increment = self.display_surface.get_size()[0] // self.attribute_number
            left = (increment * item) + (increment - self.width) // 2
            top = self.height * 0.125

        # create an items
            item = Item(left, top, self.width, self.height, index, self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.cooldown()
        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = list(self.player.stats.values())[index]
            max_value = self.max_values[index]
            cost = list(self.player.upgrade_cost.values())[index]
            item.display(self.display_surface, self.selection_index, name, value, max_value, cost)


class Item:
    def __init__(self, l, t, w, h, index, font):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font

    def displey_names(self, name, cost, selected, display):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        text_surf = self.font.render(name, False, color)
        text_rect = text_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 20))

        cost_surf = self.font.render(f'{int(cost)}', False, color)
        cost_rect = cost_surf.get_rect(midbottom=self.rect.midbottom + pygame.math.Vector2(0, -25))

        display.blit(text_surf, text_rect)
        display.blit(cost_surf, cost_rect)

    def displey_bar(self, surface, value, max_value, selected):
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom + pygame.math.Vector2(0, -60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        relative_number = (value/max_value) * (bottom[1] - top[1])
        value_rect = pygame.Rect(top[0] - 15, bottom[1] - relative_number, 30, 10)

        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player):
        upgrade_attribute = list(player.stats.keys())[self.index]

        if (player.exp >= player.upgrade_cost[upgrade_attribute] and
                player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]):
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.5
        if player.stats[upgrade_attribute] >= player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(self, surface, selection_num, name, value, max_value, cost):
        if selection_num == self.index:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR_ACTIVE, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.displey_names(name, cost, selection_num == self.index, surface)
        self.displey_bar(surface, value, max_value, selection_num == self.index)
