"""Module for Alien enemy"""
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, alien_invasion_engine):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = alien_invasion_engine.screen

        #Load the alien image and set its rect attribute
        self.image = pygame.image.load('graphics/alien.bmp')
        self.rect = self.image.get_rect()

        #Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the aliens exact horizontal position
        self.x_coord = float(self.rect.x)
