"""Module for Alien enemy"""
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, alien_invasion_engine):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = alien_invasion_engine.screen
        self.settings = alien_invasion_engine.settings

        #Load the alien image and set its rect attribute
        self.image = pygame.image.load('graphics/alien.bmp')
        self.rect = self.image.get_rect()

        #Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the aliens exact horizontal position
        self.x_coord = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left"""
        self.x_coord += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x_coord
