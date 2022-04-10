import pygame

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, screen_rect):
        pygame.sprite.Sprite.__init__(self)

        # Need to use .convert here to make it play nicely with pygame. Not exactly sure what it does but you get a big performance
        # hit for not calling it.
        self.image = pygame.image.load("imgs/Player.png").convert()

        # by putting pos in the pygame.math.Vector2 constructor we make sure it is not sharing a reference with another entity.
        self.position = pygame.math.Vector2(pos)

        self.rect = self.image.get_rect()
        self.rect.center = self.position # Center the player's image on their position

        self.speed = 250 # pixels / second

        self.screen_rect = screen_rect

    def update(self, delta, pressed_keys):
        """Update the player's position based on the keys being pressed."""

        # Use a velocity instead of updating the player's position directly, so we
        # can normalize the direction.
        vel = pygame.math.Vector2()
        if pressed_keys[pygame.K_w]:
            vel.y -= 1
        if pressed_keys[pygame.K_s]:
            vel.y += 1
        if pressed_keys[pygame.K_a]:
            vel.x -= 1
        if pressed_keys[pygame.K_d]:
            vel.x += 1

        # If the player wants to move, move them at `self.speed` pixels/second
        if vel.magnitude() != 0:
            self.position += vel.normalize() * self.speed * delta
            self.rect.center = self.position

        # Prevent them from wandering off screen. Keep track of the old
        # rectangle so we can tell if the clamp actually modified the rect.
        old_rect = self.rect.copy()
        self.rect.clamp_ip(self.screen_rect)
        if old_rect != self.rect:
            # If we always update the position, any time the player moves
            # less than 1 pixel in the positive direction, it will round down
            # (since Rects use integer coordinates)
            self.position.update(self.rect.center) 

    def shoot_at(self, aiming_pos):
        """Returns the position and direction of a bullet fired from the center
        of the player towards aiming_pos.
        """
        pos = pygame.math.Vector2(self.position)
        vel = (pygame.math.Vector2(aiming_pos) - self.position).normalize()

        return pos, vel