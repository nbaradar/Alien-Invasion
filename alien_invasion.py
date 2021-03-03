"""This is an example module.

This module does stuff.
"""

import sys
import pygame
import random

class AlienInvasion:
    """Overrall class to manage game assets and behavior"""

    #This is like the constructor for python, self refers to an instance of this class. 
    #It is automatically passed into the constructor in other programming languages.
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.pygameSurface = pygame.display.set_mode((1200, 800))


    def run_game(self):
        """Start the main loop for the game"""
        while True:
            #Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.pygameSurface.fill((random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)))

            #Make the most recently drawn screen visible
            pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
