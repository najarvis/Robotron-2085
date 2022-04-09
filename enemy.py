import pygame

class BaseEnemy(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("imgs/Enemy.png").convert()

        self.position = pygame.math.Vector2(pos)
        self.speed = 50

        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self, delta, main_player):
        """Updates the position of the enemy"""

        # Move directly towards the player's current position
        vel = (main_player.position - self.position).normalize()
        self.position += vel * self.speed * delta

        self.rect.center = self.position