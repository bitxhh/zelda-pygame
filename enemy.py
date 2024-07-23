import pygame
from settings import *
from entity import Entity


class Enemy(Entity):
    def __init__(self, groups):
        super().__init__(groups)