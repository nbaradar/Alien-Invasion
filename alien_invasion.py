"""This is an example module.

This module does stuff.
"""

import sys
from time import sleep

import pygame

#This imports the Settings class from the settings module (which is just the settings.py file)
from settings_module import Settings
from gamestats_module import GameStats
from scoreboard_module import Scoreboard
from button_module import Button
from ship_module import Ship
from bullet_module import Bullet
from alien_module import Alien

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

        self.pygame_surface = pygame.display.set_mode((self.settings.screen_width,
                                                       self.settings.screen_height))

        #Create instance to store game statistics
        self.stats = GameStats(self)

        #Create an instance of scoreboard to store the current score
        self.current_score = Scoreboard(self)

        pygame.display.set_caption("Alien Invasion")

        self.bg_color = (self.settings.bg_color)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Make the play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            #Watch for keyboard and mouse events.
            self._check_events()

            if self.stats.game_active:
                #Update the ship object
                self.ship.update()
                #Update the group of bullet objects
                self._update_bullets()
                #Update the alien objects
                self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                #If the game is inactive and you hit the play button reset
                if self._check_play_button(mouse_pos) and self.stats.game_active is False:
                    #Hide the mouse cursor
                    pygame.mouse.set_visible(False)
                    self.stats.game_active = True
                        #Reset game if play button is hit
                    if self._check_play_button(mouse_pos):
                        self.stats.reset_stats()
                        self.aliens.empty()
                        self.bullets.empty()
                        self._create_fleet()
                        self.ship.center_ship()
                        #Calling this after resetting gamestats to render scoreboard with new stats
                        self.current_score.prep_score()
                        self.current_score.prep_level()
                        self.current_score.prep_ships()
                        #Reset the games dynamic settings that were changed during previous gameplay
                        self.settings.initialize_dynamic_settings()


    def _check_play_button(self, mouse_pos):
        """Check if the mouse is within the button"""
        if self.play_button.rect.collidepoint(mouse_pos):
            return True
        else:
            return False

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

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        #Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)

            self.current_score.prep_score()
            self.current_score.check_high_score()

        #Checking if any aliens are left
        if not self.aliens:
            #Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #Increase level
            self.stats.level += 1
            self.current_score.prep_level()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 1:
            #Decrement ships_left.
            self.stats.ships_left -= 1
            self.current_score.prep_ships()

            #Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then
        update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        #Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        #Create an alien and find the number of aliens in a row.
        #Spacing between each alien is equal to one alien width
        #make the alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3* alien_height) - ship_height)
        number_rows = available_space_y // (3 * alien_height)

        #Create the full fleet of aliens
        for row_number in range(number_rows):
            #Create the first row of aliens
            for alien_number in range(number_aliens_x):
                #Create an alien and place it in the row
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Creats an alien and places it in the row"""
        alien = Alien(self)
        alien.x_coord = alien.rect.width + 2 * alien.rect.width * alien_number
        alien.rect.x = alien.x_coord
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        #First draw the updates you want onto the screen
        #self.pygame_surface.fill(self.bg_color)
        self.pygame_surface.fill(self.bg_color)
        self.ship.blitme()

        for bullet in self.bullets:
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        #Draw current score
        self.current_score.show_score()

        #Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        #Then make the most recently drawn screen visible
        pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
