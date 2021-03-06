"""Represents a bullet shot by the player"""
import pygame
from pygame.sprite import Sprite

#In python, inheritance works by passing the parent class into the child class.
#In this case, the pygame Sprite class will be a parent of this Bullet class.
class Bullet(Sprite):
    """A class to manage bullets fired from the player ship"""

    def __init__(self, alien_invasion_engine):
        """Create a bullet object at the ships current position"""
        #We call this to inheret properly from the Sprite class
        super().__init__()

        self.screen = alien_invasion_engine.screen
        self.settings = alien_invasion_engine.settings
        self.color = self.settings.bullet_color

        #Create a bullet rect at (0, 0) and then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                      self.settings.bullet_height)
        self.rect.midtop = alien_invasion_engine.ship.rect.midtop

        #Store the bullets position as a decimal value
        self.y_coord = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen"""
        #Update the decimal position of the bullet based on the speed setting
        self.y_coord -= self.settings.bullet_speed
        #Now update the rect position with the new decimal position of the bullet
        self.rect.y = self.y_coord

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
