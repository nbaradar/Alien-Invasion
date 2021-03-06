"""This is an example module.

This module does stuff.
"""

import sys
import pygame

#This imports the Settings class from the settings module (which is just the settings.py file)
from settings_module import Settings
from ship_module import Ship
from bullet_module import Bullet

class AlienInvasion:
    """Overrall class to manage game assets and behavior"""

    #This is like the constructor for python, self refers to an instance of this class.
    #It is automatically passed into the constructor in other programming languages.
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        #Initialize settings option as a variable
        self.settings = Settings()

        #Runs the game in fullscreen
        self.screen= pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.pygame_surface = pygame.display.set_mode((self.settings.screen_width,
                                                       self.settings.screen_height))
        self.bg_color = (self.settings.bg_color)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            #Watch for keyboard and mouse events.
            self._check_events()
            #Update the ship object
            self.ship.update()
            #Update the group of bullet objects
            self._update_bullets()
            #Draw the screen
            self._update_screen()

    def _check_events(self):
        """Listens for button/mouse events and responds accordingly."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """Respond to KEYDOWN events"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        #If the user presses q, quit
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to KEYUP events"""
        if event.key == pygame.K_RIGHT or event.key== pygame.K_LEFT:
            self.ship.moving_right = False
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the group of bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of the bullets and get rid of old bullets"""
        #Update bullet positions.
        #(Calling update Group parent class invokes update in the child aka. bullets)
        self.bullets.update()

        #Get rid of bullets that have reached top of screen
        for bullet in self.bullets:
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        #First draw the updates you want onto the screen
        #self.pygame_surface.fill(self.bg_color)
        self.pygame_surface.fill(self.bg_color)
        self.ship.blitme()

        for bullet in self.bullets:
            bullet.draw_bullet()

        #Then make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
