"""This is an example module.

This module does stuff.
"""

import sys
import pygame
import random

#This imports the Settings class from the settings module (which is just the settings.py file)
from settingsModule import Settings
from shipModule import Ship

class AlienInvasion:
    """Overrall class to manage game assets and behavior"""

    #This is like the constructor for python, self refers to an instance of this class. 
    #It is automatically passed into the constructor in other programming languages.
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        pygame.display.set_caption("Alien Invasion")
        
        self.settings = Settings()
        self.pygameSurface = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.bg_color = (self.settings.bg_color)
        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            #Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.pygameSurface.fill(self.bg_color)
                    """self.pygameSurface.fill((random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)))"""
                    
            self.ship.blitme()
                    
            #Make the most recently drawn screen visible
            pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
