import pygame
import helper_funcs

class Bullet(pygame.sprite.Sprite):
    """Bullet fired from the player. Travels at a constant speed in a straight line until
    it goes off the screen or intersects with an enemy.
    """

    def __init__(self, pos: helper_funcs.CoordType, vel: pygame.math.Vector2, screen_rect: pygame.Rect, explosion_sound: pygame.mixer.Sound):
        pygame.sprite.Sprite.__init__(self)

        # TODO: Maybe make pos and vel the same type to avoid confusion
        self.position = pygame.math.Vector2(pos)
        self.velocity = vel
        self.speed = 1000

        self.image = self.get_bullet_image()

        self.rect = self.image.get_rect()
        self.rect.center = self.position

        # Rectangle representing the bounds of the screen
        self.screen_rect = screen_rect

        self.explosion_sound = explosion_sound

    def update(self, delta: float, enemies: pygame.sprite.Group) -> None:
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
            self.explosion_sound.play()

    def get_bullet_image(self) -> pygame.Surface:
        """Create an image and align it along the direction the bullet is traveling"""

        # Create an image large enough to hold the rotated bullet
        length = 24 # pixels
        w = max(abs(self.velocity.x * length), 1)
        h = max(abs(self.velocity.y * length), 1)
        bullet_image = pygame.Surface((w, h))

        # Calculate the coordinates of the start and end of the line
        # by starting in the center and going half the length in the self.velocity
        # and the -self.velocity directions.
        start_vec = pygame.math.Vector2((w / 2, h / 2))
        offset_vec = self.velocity * (length / 2)
        pygame.draw.line(bullet_image, (255, 255, 255), start_vec - offset_vec, start_vec + offset_vec)
        return bullet_image
