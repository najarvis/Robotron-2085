from datetime import datetime
import pygame

from enemy import Electrode, Grunt
from family import FamilyMember
from director import Director, EnemyType
from player import Player

import helper_funcs

# "Global" variables
SCREEN_SIZE = WIDTH, HEIGHT = (800, 800)
SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)

def run() -> None:
    """Put the main game logic in a function, to make it more `pythonic`"""

    # -- Setup --
    pygame.init()
    pygame.joystick.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("ROBOTRON: 2085")

    clock = pygame.time.Clock()
    done = False

    # Game director holds the state of the game, and handles the major functions.
    game_director = Director(SCREEN_RECT)

    level1_dict = {
        Electrode:    helper_funcs.generate_rand_coords(SCREEN_RECT, 10),
        Grunt:        helper_funcs.generate_rand_coords(SCREEN_RECT, 10),
        Player:       [SCREEN_RECT.center],
        FamilyMember: helper_funcs.generate_rand_coords(SCREEN_RECT, 5)
    }
    game_director.load_level(level1_dict)

    if pygame.joystick.get_count() > 0:
        game_director.set_joystick(game_director.init_joystick(0))

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

                if event.key == pygame.K_F2:
                    pygame.image.save(screen, "screenshots/screenshot_{}.png".format(datetime.now().strftime('%Y-%m-%dT%H%M%S')))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    game_director.shoot(event.pos)

            if event.type == pygame.JOYDEVICEADDED:
                if game_director.joystick is None:
                    game_director.set_joystick(game_director.init_joystick(event.device_index))

            # TODO: Make robust against multiple joysticks / controllers being plugged in / removed
            elif event.type == pygame.JOYDEVICEREMOVED:
                if game_director.joystick is not None:
                    game_director.remove_joystick()
                    
        # Update all entities
        pressed_keys = pygame.key.get_pressed()
        game_director.update(delta, pressed_keys)

        # Fill the screen with black to reset it.
        screen.fill((0, 0, 0))

        game_director.draw(screen)

        pygame.display.update()

    # -- Clean Up --
    pygame.quit()

# Use the standard way of calling our code. Prevents this from being an issue if imported.
if __name__ == "__main__":
    run()