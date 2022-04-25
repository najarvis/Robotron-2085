import pygame
import helper_funcs

class Destroyed(pygame.sprite.Sprite):

    def __init__(self, position: helper_funcs.CoordType, velocity: pygame.math.Vector2, image: pygame.Surface, screen_rect: pygame.Rect):
        pygame.sprite.Sprite.__init__(self)
        self.position = position.copy()
        self.image = image
        self.velocity = velocity
        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self.screen_rect = screen_rect
        self.speed = 150
        self.lifetime = 0.5 # Maximum lifetime of the sprite, will kill itself after this many seconds

    def update(self, delta):
        self.position += self.velocity * self.speed * delta
        self.rect.center = self.position

        # If we are not colliding with the screen rectangle, we are outside of
        # it, and thus the bullet can despawn
        if not self.screen_rect.colliderect(self.rect):
            self.kill()

        self.lifetime -= delta
        if self.lifetime <= 0:
            self.kill()


class DestroyedEntityFactory:
    """When an entity in robotron is destroyed, it splits apart into slices
    that spread apart on the screen. This factory class is designed to help
    facilitate generating the slices."""


    @staticmethod
    def create_destroyed_entities(output: pygame.sprite.Group, position: helper_funcs.CoordType,
                                  image: pygame.Surface, screen_rect: pygame.Rect,
                                  horizontal: bool = True):
        slice_size = 4 #px/row
        image_size = image.get_size()
        if horizontal:
            dimension = image_size[0]
        else:
            dimension = image_size[1]

        num_slices = dimension // slice_size
        for slice_index in range(num_slices):
            if horizontal:
                subsurf_rect = pygame.Rect(0, slice_index * slice_size, image_size[0], slice_size)
                vel = pygame.math.Vector2(0, num_slices / 2 - (slice_index + 0.5))

            else:
                subsurf_rect = pygame.Rect(slice_index * slice_size, 0, slice_size, image_size[1])
                vel = pygame.math.Vector2(num_slices / 2 - (slice_index + 0.5), 0)

            output.add(Destroyed(position, vel, image.subsurface(subsurf_rect), screen_rect))