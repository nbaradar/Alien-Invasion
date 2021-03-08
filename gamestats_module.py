"""Tracks the games statistics"""

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, alien_invasion_engine):
        """Initialize statistics."""
        self.settings = alien_invasion_engine.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize the statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
