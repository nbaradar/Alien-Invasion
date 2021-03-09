"""Module for player ship"""

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""
    #The contructor takes the game engine so it has access to all its resources
    def __init__(self, alien_invasion_engine):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = alien_invasion_engine.pygame_surface
        self.screen_rect = alien_invasion_engine.pygame_surface.get_rect()
        self.settings = alien_invasion_engine.settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('graphics\ship.bmp')
        self.rect = self.image.get_rect()

        #Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a decimal value for the ships current position
        self.x_coord = float(self.rect.x)

        #Movement flag
        self.moving_right = False
        #Movement flag
        self.moving_left = False


        self.speed = self.settings.ship_speed

    def update(self):
        """Update the ships position based on the movement of the flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x_coord += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x_coord -= self.settings.ship_speed

        #Update rect object from self.x
        self.rect.x = self.x_coord

    def blitme(self):
        """Draw the ship at its current position."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x_coord = float(self.rect.x)
