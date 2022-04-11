import pygame
import random
import math
from typing import Union

from player import Player
from bullet import Bullet
from enemy import BaseEnemy, Electrode, Grunt
from family import FamilyMember

import helper_funcs

# "Global" variables
SCREEN_SIZE = WIDTH, HEIGHT = (800, 800)
SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)

# I haven't done this before, but I'm learning type annotation in Python.
# This is basically saying the type could be any of these.
EnemyType = Union[BaseEnemy, Electrode, Grunt]

def run() -> None:
    """Put the main game logic in a function, to make it more `pythonic`"""

    # -- Setup --
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("ROBOTRON: 2085")

    clock = pygame.time.Clock()
    done = False

    shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
    explosion_sound = pygame.mixer.Sound("sounds/explode.wav")

    # -- Groups --
    main_player = Player(SCREEN_RECT.center, SCREEN_RECT)
    player_group = pygame.sprite.Group(main_player)

    bullet_group = pygame.sprite.Group()

    generate_enemies(enemies := [], 20)
    enemy_group = pygame.sprite.Group(*enemies)

    generate_family(family_members := [], 4)
    family_group = pygame.sprite.Group(*family_members)

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
                    pos, vel = helper_funcs.shoot_at(main_player.position, event.pos)
                    new_bullet = Bullet(pos, vel, SCREEN_RECT, explosion_sound)
                    bullet_group.add(new_bullet)
                    shoot_sound.play()
                    
        # Update all entities
        pressed_keys = pygame.key.get_pressed()
        player_group.update(delta, pressed_keys)
        bullet_group.update(delta, enemy_group)
        enemy_group.update(delta, main_player)
        family_group.update(delta)

        # Resolve player colisions here now that everything is done moving
        if (collided_enemy := pygame.sprite.spritecollideany(main_player, enemy_group)) is not None:
            # main_player.kill()
            print("YOU DIED")

        # Fill the screen with black to reset it.
        screen.fill((0, 0, 0))

        # Draw all entities
        family_group.draw(screen)
        player_group.draw(screen)
        bullet_group.draw(screen)
        enemy_group.draw(screen)

        pygame.display.update()

    # -- Clean Up --
    pygame.quit()

def generate_enemies(enemy_array: list[EnemyType], num: int) -> None:
    """Generates `num` enemies randomly around the center of the screen and adds them to `enemy_array`"""
    min_dimension = min(WIDTH, HEIGHT)
    min_radius = min_dimension / 4
    max_radius = min_dimension / 2
    for _ in range(num):
        enemy_pos = helper_funcs.random_radial_coord(SCREEN_RECT.center, min_radius, max_radius)
        enemy_type = random.choice([Grunt, Electrode])
        enemy_array.append(enemy_type(enemy_pos, SCREEN_RECT))

def generate_family(family_array: list[FamilyMember], num: int) -> None:
    """Generates `num` FamilyMembers randomly around the center of the screen and adds them to `family_array`"""
    min_dimension = min(WIDTH, HEIGHT)
    min_radius = min_dimension / 4
    max_radius = min_dimension / 2
    for _ in range(num):
        family_pos = helper_funcs.random_radial_coord(SCREEN_RECT.center, min_radius, max_radius)
        family_array.append(FamilyMember(family_pos, SCREEN_RECT))

# Use the standard way of calling our code. Prevents this from being an issue if imported.
if __name__ == "__main__":
    run()