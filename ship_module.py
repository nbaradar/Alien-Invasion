"""Module for player ship"""

import pygame

class Ship:
    """A class to manage the ship."""
    #The contructor takes the game engine so it has access to all its resources
    def __init__(self, alienInvasion_engine):
        """Initialize the ship and set its starting position."""
        self.screen = alienInvasion_engine.pygameSurface
        self.screen_rect = alienInvasion_engine.pygameSurface.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('graphics\ship.bmp')
        self.rect = self.image.get_rect()

        #Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship at its current position."""
        self.screen.blit(self.image, self.rect)
