import pygame
import helper_funcs

class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos: helper_funcs.CoordType, screen_rect: pygame.Rect):
        pygame.sprite.Sprite.__init__(self)

        # Need to use .convert here to make it play nicely with pygame. Not 
        # exactly sure what it does but you get a big performance hit for not 
        # calling it.
        self.image = pygame.image.load("imgs/Player.png").convert()

        # by putting pos in the pygame.math.Vector2 constructor we make sure it
        # is not sharing a reference with another entity.
        self.position = pygame.math.Vector2(pos)

        self.rect = self.image.get_rect()
        self.rect.center = self.position # Center the player's image on their position

        self.speed = 250 # pixels / second

        self.screen_rect = screen_rect

    def update(self, delta: float, pressed_keys: list[bool]) -> None:
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

        # To avoid conditionals we could rewrite the above as:
        # vel.y += int(pressed_keys[pygame.K_s]) - int(pressed_keys[pygame.K_w])
        # vel.x += int(pressed_keys[pygame.K_d]) - int(pressed_keys[pygame.K_a])

        # If the player wants to move, move them at `self.speed` pixels/second
        if vel.magnitude() != 0:
            self.position += vel.normalize() * self.speed * delta
            self.rect.center = self.position

        helper_funcs.affix_to_screen(self)
