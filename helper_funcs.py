import pygame
import random

CoordType = tuple[int, int] | tuple[float, float] | pygame.math.Vector2

def affix_to_screen(sprite_obj: pygame.sprite.Sprite) -> None:
    """Prevents a sprite from wandering off screen. Keeps track of the old
    rectangle so we only update the position if the clamp modified the rect.
    """

    assert sprite_obj is not None
    assert sprite_obj.rect is not None
    assert sprite_obj.screen_rect is not None
    assert sprite_obj.position is not None

    old_rect = sprite_obj.rect.copy()
    sprite_obj.rect.clamp_ip(sprite_obj.screen_rect)
    if old_rect != sprite_obj.rect:
        # If we always updated the position, any time the player moved
        # less than 1 pixel in the positive direction it would round back down
        # (since Rects use integer coordinates)
        sprite_obj.position.update(sprite_obj.rect.center)


def shoot_at(start_pos: CoordType, aiming_pos: CoordType) -> tuple[pygame.math.Vector2, pygame.math.Vector2]:
    """Returns the position and direction of a bullet fired from the center
    of the player towards aiming_pos.
    """
    pos = pygame.math.Vector2(start_pos)
    vel = (pygame.math.Vector2(aiming_pos) - pos).normalize()

    return pos, vel

def random_radial_coord(center: CoordType, min_radius: float, max_radius: float) -> pygame.math.Vector2:
    """Returns a random coordinate between min_radius and max_radius pixels away from center"""

    random_angle = random.uniform(0, 360) # random angle on unit circle
    random_dist = random.uniform(min_radius, max_radius) # Spawn anywhere from the edge of the map to halfway to the player
    return pygame.math.Vector2(center) + vec2_from_polar(random_dist, random_angle)

def vec2_from_polar(r: float, phi: float):
    """Returns a Vector2 r units away and phi degrees offset from the origin"""

    vec = pygame.math.Vector2()
    vec.from_polar((r, phi))
    return vec

def generate_rand_coords(spawn_rect: pygame.Rect, num: int, min_percent: float = 0.5, max_percent: float = 1.0) -> list[tuple[float, float]]:
    min_dim = min(spawn_rect.width, spawn_rect.height)
    min_radius = min_dim * min_percent / 2
    max_radius = min_dim * max_percent / 2
    return [random_radial_coord(spawn_rect.center, min_radius, max_radius) for _ in range(num)]