import pygame
import random
import math

from player import Player
from bullet import Bullet
from enemy import BaseEnemy

# "Global" variables
SCREEN_SIZE = WIDTH, HEIGHT = (1600, 900)
SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)

def run():
    """Put the main game logic in a function, to make it more `pythonic`"""

    # -- Setup --
    # Moved this into the function, no need for it to be a global variable, don't want 
    # to initialize the video if this file is imported.
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    done = False

    # -- Groups --
    main_player = Player(SCREEN_RECT.center)
    player_group = pygame.sprite.Group(main_player)

    bullet_group = pygame.sprite.Group()

    generate_enemies(enemies := [], 20)
    enemy_group = pygame.sprite.Group(*enemies)

    # -- Main game loop --
    while not done:
        delta = clock.tick(60) / 1000.0 # Time passed since the last frame in SECONDS

        # Loop through all game events
        for event in pygame.event.get():

            # Close the application if the user hits the X in the top right corner
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                # Close the application if the user hits the ESC key
                if event.key == pygame.K_ESCAPE:
                    done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    # Get the components for the new bullet
                    pos, vel = main_player.shoot_at(event.pos)
                    new_bullet = Bullet(pos, vel, SCREEN_RECT)
                    bullet_group.add(new_bullet)
                    
        # Update all entities
        pressed_keys = pygame.key.get_pressed()
        player_group.update(delta, pressed_keys)
        bullet_group.update(delta, enemy_group)
        enemy_group.update(delta, main_player)

        # Resolve player colisions here now that everything is done moving
        if (collided_enemy := pygame.sprite.spritecollideany(main_player, enemy_group)) is not None:
            main_player.kill()
            print("YOU DIED")

        # Fill the screen with black to reset it.
        screen.fill((0, 0, 0))

        # Draw all entities
        player_group.draw(screen)
        bullet_group.draw(screen)
        enemy_group.draw(screen)

        pygame.display.update()

def generate_enemies(enemy_array, num):
    """Generates `num` enemies randomly around the center of the screen and adds them to `enemy_array`"""
    min_dimension = min(WIDTH, HEIGHT)
    for i in range(num):
        random_angle = random.uniform(0, math.pi * 2) # random angle on unit circle
        random_dist = random.uniform(min_dimension / 4, min_dimension / 2) # Spawn anywhere from the edge of the map to halfway to the player
        enemy_pos_x = SCREEN_RECT.centerx + math.cos(random_angle) * random_dist
        enemy_pos_y = SCREEN_RECT.centery + math.sin(random_angle) * random_dist
        enemy_array.append(BaseEnemy((enemy_pos_x, enemy_pos_y)))

# Use the standard way of calling our code. Prevents this from being an issue if imported.
if __name__ == "__main__":
    run()