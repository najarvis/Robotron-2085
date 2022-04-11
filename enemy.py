import pygame
import helper_funcs
from player import Player

class BaseEnemy(pygame.sprite.Sprite):

    reward: int = 0

    def __init__(self, pos: helper_funcs.CoordType, screen_rect: pygame.Rect):
        pygame.sprite.Sprite.__init__(self)

        # TODO: Don't load the images each time an enemy is instantiated. Load them once elsewhere and pass them in.
        self.image: pygame.Surface = pygame.image.load("imgs/Enemy.png").convert()

        self.position = pygame.math.Vector2(pos)
        self.speed: int = 50

        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self.screen_rect = screen_rect

    def update(self, delta: float, main_player: Player) -> None:
        """Updates the position of the enemy"""

        # Move directly towards the player's current position
        vel = (main_player.position - self.position).normalize()
        self.position += vel * self.speed * delta

        self.rect.center = self.position
        helper_funcs.affix_to_screen(self)

class Electrode(BaseEnemy):
    """Stationary. Can be destroyed by player by shooting."""

    reward = 100

    def __init__(self, pos: helper_funcs.CoordType, screen_rect: pygame.Rect):
        BaseEnemy.__init__(self, pos, screen_rect)
        self.speed = 0
        self.image = pygame.Surface(self.image.get_size())
        self.image.fill((255, 255, 255))

class Grunt(BaseEnemy):
    """Moves towards player in a straight line. Can be destroyed by player by shooting."""

    reward = 200

    def __init__(self, pos: helper_funcs.CoordType, screen_rect: pygame.Rect):
        BaseEnemy.__init__(self, pos, screen_rect)
        self.speed = 100