import pygame

class Bullet(pygame.sprite.Sprite):
    """Bullet fired from the player's gun. Travels at a constant speed in a straight line until
    it goes off the screen or intersects with an enemy.
    """

    def __init__(self, pos, vel, screen_rect):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((32, 8))
        self.image.fill((255, 255, 255))

        self.position = pygame.math.Vector2(pos)
        self.velocity = vel
        self.speed = 1000

        self.rect = self.image.get_rect()
        self.rect.center = self.position

        # Rectangle representing the bounds of the screen
        self.screen_rect = screen_rect

    def update(self, delta, enemies):
        self.position += self.velocity * self.speed * delta
        self.rect.center = self.position

        # If we are not colliding with the screen rectangle, we are outside of it, and thus the bullet can despawn
        if not self.screen_rect.colliderect(self.rect):
            self.kill()

        # Check if we collide with any enemies. Walrus operator here returns what collided_enemy is set to,
        # Which is None in the event of no collision or an enemy sprite if there is one.
        if (collided_enemy := pygame.sprite.spritecollideany(self, enemies)) is not None:
            collided_enemy.kill()
            self.kill()
