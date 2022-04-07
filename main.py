import pygame
import random

from player import Player
from bullet import Bullet
from enemy import Enemy

# "Global" variables
SCREEN_SIZE = WIDTH, HEIGHT = (1600, 900)
SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)

def run():
    """Put the main game logic in a function, to make it more `pythonic`"""
    
    # Moved this into the function, no need for it to be a global variable, don't want 
    # to initialize the video if this file is imported.
    screen = pygame.display.set_mode(SCREEN_SIZE)

    done = False

    main_player = Player((32, 32))
    player_group = pygame.sprite.Group(main_player)

    bullet_group = pygame.sprite.Group()

     # 20 enemies spawn randomly on the right half of the screen
    enemies = [Enemy((random.randint(WIDTH / 2, WIDTH), 
                    random.randint(0, HEIGHT))) for i in range(20)]

    enemy_group = pygame.sprite.Group(*enemies)

    clock = pygame.time.Clock()

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

        # Fill the screen with black to reset it.
        screen.fill((0, 0, 0))

        # Draw all entities
        player_group.draw(screen)
        bullet_group.draw(screen)
        enemy_group.draw(screen)

        pygame.display.update()

# Use the standard way of calling our code. Prevents this from being an issue if imported.
if __name__ == "__main__":
    run()