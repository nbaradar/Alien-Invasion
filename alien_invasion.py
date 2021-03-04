"""This is an example module.

This module does stuff.
"""

import sys
import random
import pygame

#This imports the Settings class from the settings module (which is just the settings.py file)
from settings_module import Settings
from ship_module import Ship

class AlienInvasion:
    """Overrall class to manage game assets and behavior"""

    #This is like the constructor for python, self refers to an instance of this class.
    #It is automatically passed into the constructor in other programming languages.
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        pygame.display.set_caption("Alien Invasion")

        #Initialize settings option as a 
        self.settings = Settings()
        self.pygame_surface = pygame.display.set_mode((self.settings.screen_width,
                                                       self.settings.screen_height))
        self.bg_color = (self.settings.bg_color)
        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            #Watch for keyboard and mouse events.
            self._check_events()
            #Draw the screen
            self._update_screen()

    def _check_events(self):
        """Listens for button/mouse events and responds accordingly."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.pygame_surface.fill((random.randrange(0,255),
                                          random.randrange(0,255),
                                          random.randrange(0,255)))

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        #First draw the updates you want onto the screen
        #self.pygame_surface.fill(self.bg_color)
        self.ship.blitme()

        #Then make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
