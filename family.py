import pygame
import random

class FamilyMember(pygame.sprite.Sprite):
    """Family members wander the screen, waiting to be rescued by the player.
    Can be killed by Hulks. When the player contacts a family member they get 200*x^n points,
    where x is how many other family members they've picked up during that level.
    """

    VELOCITY_OPTS = [pygame.math.Vector2((0, 0)),
                     pygame.math.Vector2((1, 0)),
                     pygame.math.Vector2((0, 1)),
                     pygame.math.Vector2((-1, 0)),
                     pygame.math.Vector2((0, -1))]

    def __init__(self, pos, screen_rect):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 255, 0))

        self.position = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2()
        self.speed = 50

        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self.direction_timer = 0
        self.direction_timer_max = 2

        self.screen_rect = screen_rect

    def update(self, delta):
        # Move in the same direction for self.direction_timer_max seconds, then
        # pick a new direction (or none, if the (0, 0) vector is chosen)
        self.direction_timer -= delta
        if self.direction_timer <= 0:
            self.velocity = random.choice(FamilyMember.VELOCITY_OPTS)
            self.direction_timer = self.direction_timer_max

        self.position += self.velocity * self.speed * delta
        self.rect.center = self.position

        # Prevent them from wandering off screen. Keep track of the old
        # rectangle so we can tell if the clamp actually modified the rect.
        old_rect = self.rect.copy()
        self.rect.clamp_ip(self.screen_rect)
        if old_rect != self.rect:
            # If we always update the position, any time the FamilyMember moves
            # less than 1 pixel in the positive direction, it will round down
            # (since Rects use integer coordinates)
            self.position.update(self.rect.center) 